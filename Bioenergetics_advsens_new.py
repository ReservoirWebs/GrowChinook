#!/usr/bin/python

import pylab
import glob
import time
import os
import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate import trapz
from scipy.optimize import minimize_scalar
from csv import DictReader, QUOTE_NONNUMERIC
from collections import defaultdict
from matplotlib import pyplot
from datetime import datetime, timedelta

#Minimum and maximum elevations for each reservoir
FC_MAX_EL = 833.3
FC_MIN_EL = 682.2
HC_MAX_EL = 1545.3
HC_MIN_EL = 1246.7
LP_MAX_EL = 931.7
LP_MIN_EL = 715.2


def scruffy(path,return_path,name): #Scruffy's the janitor. Kills any output files older than one hour
    os.chdir(path)
    hour_ago = datetime.now() - timedelta(hours=1)
    for file in glob.glob("{}*".format(name)):
        age = datetime.fromtimestamp(os.path.getctime(file))
        if age < hour_ago:
            os.remove(file)
    os.chdir(return_path)

def get_sustain_est(elevation, total_daphnia, consumed, site):
    bath_data = '{}Bath.csv'.format(site)
    bath = {}
    with open(bath_data) as file:
        reader = DictReader(file)
        for row in reader:
            bath.update({int(row['elevation (m)']): float(row[' 2d_area (m2)'])})
    if site == 'Fall Creek':
        elev = min(max((elevation/3.281), (FC_MIN_EL/3.281)), (FC_MAX_EL/3.281))
    elif site == 'Hills Creek':
        elev = min(max((elevation/3.281), (HC_MIN_EL/3.281)), (HC_MAX_EL/3.281))
    elif site == 'Lookout Point':
        elev = min(max((elevation/3.281), (LP_MIN_EL/3.281)), (LP_MAX_EL/3.281))
    area = bath[int(elev)]
    consumable = (area*total_daphnia*0.58)
    pop_est = consumable/(consumed*4)
    return pop_est


def get_vals(light_in, total_daphnia_in, daphnia_size_in, site, month, year):
    #k represents the light extinction coefficient
    lights = {('Fall Creek', '2016'): {'April': 0.758, 'May': 0.466, 'June': 0.435,
                                       'July': 0.451, 'August': 0.444, 'September': 0.406},
              ('Hills Creek', '2016'): {'April': 0.399, 'May': 0.321, 'June': 0.440,
                                        'July': 0.257, 'August': 0.384, 'September': 0.340},
              ('Lookout Point', '2016'): {'April': 0.514, 'May': 0.373, 'June': 0.368,
                                          'July': 0.311, 'August': 0.389, 'September': 0.343},
              ('Fall Creek', '2015'): {'March': 0.834, 'April': 0.596, 'May': 0.58, 'June': 0.72,
                                       'July': 0.521, 'August': 0.509},
              ('Hills Creek', '2015'): {'March': 0.583, 'April': 0.503, 'May': 0.467,
                                        'June': 0.441, 'July': 0.32, 'August': 0.368},
              ('Lookout Point', '2015'): {'March': 0.532, 'April': 0.565, 'May': 0.373,
                                          'June': 0.374, 'July': 0.396, 'August': 0.39},
              ('Fall Creek', '2014'): {'June': 0.404, 'July': 0.274, 'August': 0.295},
              ('Hills Creek', '2014'): {'June': 0.298, 'July': 0.274, 'August': 0.274},
              ('Lookout Point', '2014'): {'June': 0.315, 'July': 0.271, 'August': 0.282}
             }

    # Daphnia totals weighted by subsample - only from C and Z sites
    # July 2013 and July 2014 are not currently available
    daphnias = {('Fall Creek', '2016'): {'April': 367, 'May': 22328, 'June': 48240, 'July': 8801,
                                         'August': 5378, 'September': 3626},
                ('Hills Creek', '2016'): {'April': 163, 'May': 7456, 'June': 88658, 'July': 9045,
                                          'August': 13527, 'September': 13853},
                ('Lookout Point', '2016'): {'April': 20, 'May': 448, 'June': 9290, 'July': 11693,
                                            'August': 6926, 'September': 1854},
                ('Fall Creek', '2015'): {'March': 815, 'April': 17357, 'May': 24446, 'June':3993,
                                         'July': 2363, 'August': 407},
                ('Hills Creek', '2015'): {'March': 204, 'April': 453, 'May': 11408, 'June': 20535,
                                          'July': 9126, 'August': 3178},
                ('Lookout Point', '2015'): {'March': 61, 'April': 127, 'May': 14016, 'June': 44981,
                                            'July': 5949, 'August': 581},
                ('Fall Creek', '2014'): {'June': 25280, 'July': 0, 'August': 7752},
                ('Hills Creek', '2014'): {'June': 6040, 'July': 0, 'August': 2249},
                ('Lookout Point', '2014'): {'June': 16863, 'July': 0, 'August': 1061},
                ('Fall Creek', '2013'): {'June': 18416, 'July': 0, 'August': 4563},
                ('Hills Creek', '2013'): {'June': 127772, 'July': 0, 'August': 18559},
                ('Blue River', '2013'): {'June': 68449, 'July': 0, 'August': 41233}
               }

#Weighted for proportion D.mendotae, D.pulex, and D.rosea/ambigua averaged across available years
    sizes = {('Fall Creek', '2016'): {'April': 0.56, 'May': 1.01, 'June': 1.13, 'July': 1.48,
                                      'August': 1.78, 'September': 1.10},
             ('Hills Creek', '2016'): {'April': 1.22, 'May': 1.08, 'June': 1.16, 'July': 1.54,
                                       'August': 1.18, 'September': 1.51},
             ('Lookout Point', '2016'): {'April': 0.53, 'May': 0.68, 'June': 1.14, 'July': 1.31,
                                         'August': 1.64, 'September': 1.20},
             ('Blue River', '2016'): {'July': 1.27},
             ('Fall Creek', '2015'): {'March': 1.21, 'April': 1.25, 'May': 1.13, 'June': 1.26,
                                      'July': 1.49, 'August': 1.18},
             ('Hills Creek', '2015'): {'March': 1.24, 'April': 1.09, 'May': 1.03, 'June': 1.20,
                                       'July': 1.84, 'August': 2.21},
             ('Lookout Point', '2015'): {'March': 1.46, 'April': 0.96, 'May': 1.06, 'June': 1.35,
                                         'July': 1.97, 'August': 2.07},
             ('Blue River', '2015'): {'March': 0.63, 'April': 0.73, 'May': 0.83, 'June': 1.50,
                                      'July': 1.48, 'August': 1.25},
             ('Fall Creek', '2014'): {'March': 1.207, 'April': 0.90375, 'May': 1.073, 'June': 1.262,
                                      'July': 1.485, 'August': 1.633},
             ('Hills Creek', '2014'): {'March': 1.238, 'April': 1.152, 'May': 1.058, 'June': 1.232,
                                       'July': 1.687, 'August': 2.005},
             ('Lookout Point', '2014'): {'March': 1.457, 'April': 0.745, 'May': 0.871,
                                         'June': 1.237, 'July': 1.642, 'August': 2.033},
             ('Blue River', '2014'): {'March': 0.628, 'April': 0.780, 'May': 0.827, 'June': 1.321,
                                      'July': 1.377, 'August': 1.282}
            }


    if light_in == float(123456):
        light = lights[(site, year)][month]
    else:
        light = light_in
    print(site,month,year)
    if total_daphnia_in == float(123456):
        total_daphnia = daphnias[(site, year)][month]
    else:
        total_daphnia = total_daphnia_in

    if daphnia_size_in == float(123456):
        daphnia_size = sizes[(site, year)][month]
    else:
        daphnia_size = daphnia_size_in

    return light, total_daphnia, daphnia_size


def sensitivity_expand(form):
    sparam_exp = []
    if form.getvalue('Sparam_Range') != None:
        sparam_range = float(form.getvalue('Sparam_Range'))
    else:
        sparam_range = 200
    step_size = (sparam_range-100)/1000
    for i in range(5, 1, -1):
        sparam_exp.append(float(1)/(i*10))
    sparam_exp.append(1)
    for i in range(1, 11):
        sparam_exp.append(float(1)+(step_size*i))
    return sparam_exp

def run_sensitivity(sens_factors, sparam, site_data, starting_mass, daph_data, max_temp, min_temp, cust_temp, elev, pop_site, base_val, base_set_flag):
    batches = []
    results = []
    sens_inputs = []
    growths = []
    growths1 = []
    csvheaders = [[] for i in range(20)]
    SHORT_RESULTS = {'Elevation': [], 'Reservoir(used for elevation)': [],
                     'Daphnia Density': [], 'Light': [], 'Daphnia Size': [],
                     'Min Depth': [], 'Max Depth': [], 'Min Temp': [], 'Max Temp': [],
                     'Daphnia Year': [], 'Daphnia Month': [], 'Daphnia Site': [],
                     'Temperature File': [], 'Starting Mass': [], 'Ending Mass': [],
                     'Day Depth': [], 'Day Temperature': [], 'Night Depth': [],
                     'Night Temperature': [], 'Day 1 Growth': [], 'Day 30 Growth': [],
                     'Daphnia Consumed': [], 'Sustainable Estimate': [],
                     'Estimated Condition Change': []}
    if base_set_flag == 0:    
        if sparam == 'Starting Mass':
            base_input = starting_mass
        elif sparam == 'Total Daphnia':
            base_input = daph_data.total_daph
        elif sparam == 'Daphnia Size':
            base_input = daph_data.daph_size
        else:
            base_input = site_data.light
        print("base input: ", base_input, "<br>")
        base_set_flag = 1
        base_val = base_input
    else:
        base_input = base_val


    for i in range(15):
        print("base input: ", base_input, "<br>")
        if (base_input * sens_factors[i]) > 0.00001:
            sens_inputs.append(base_input * sens_factors[i])
        else:
            sens_inputs.append(.00001)
        sens_factors[i] = sens_factors[i] * 100
        csvheaders[i] = [site_data.site, site_data.month, site_data.year, ("%s: %f" % (sparam, sens_inputs[i]))]
        if sparam == 'Starting Mass':
            batches.append(Batch(site_data, sens_inputs[i], daph_data, max_temp, min_temp, cust_temp, elev, pop_site))
        elif sparam == 'Total Daphnia':
            daph_data.total_daph = sens_inputs[i]
            batches.append(Batch(site_data, starting_mass, daph_data, max_temp, min_temp, cust_temp, elev, pop_site))
        elif sparam == 'Daphnia Size':
            daph_data.daph_size = sens_inputs[i]
            batches.append(Batch(site_data, starting_mass, daph_data, max_temp, min_temp, cust_temp, elev, pop_site))
        else:
            site_data.light = sens_inputs[i]
            batches.append(Batch(site_data, starting_mass, daph_data, max_temp, min_temp, cust_temp, elev, pop_site))

        res, taway, condition, condition1, dt, nt, taway2 = batches[i].Run_Batch()
        results.append(res)
        #SHORT_RESULTS['Tab Name'].append(vals.title)
        SHORT_RESULTS['Elevation'].append(elev)
        SHORT_RESULTS['Reservoir(used for elevation)'].append(pop_site)
        SHORT_RESULTS['Daphnia Density'].append(daph_data.total_daph)
        SHORT_RESULTS['Light'].append(site_data.light)
        SHORT_RESULTS['Daphnia Size'].append(daph_data.daph_size)
        SHORT_RESULTS['Min Depth'].append(site_data.min_depth)
        SHORT_RESULTS['Max Depth'].append(site_data.max_depth)
        SHORT_RESULTS['Min Temp'].append(min_temp)
        SHORT_RESULTS['Max Temp'].append(max_temp)
        SHORT_RESULTS['Daphnia Year'].append(daph_data.d_year)
        SHORT_RESULTS['Daphnia Month'].append(daph_data.d_month)
        SHORT_RESULTS['Daphnia Site'].append(daph_data.d_site)
        SHORT_RESULTS['Temperature File'].append(cust_temp)
        SHORT_RESULTS['Starting Mass'].append(starting_mass)
        SHORT_RESULTS['Ending Mass'].append(results[i]['StartingMass'][29])
        SHORT_RESULTS['Day Depth'].append(results[i]['day_depth'][29])
        SHORT_RESULTS['Day Temperature'].append(dt)
        SHORT_RESULTS['Night Depth'].append(results[i]['night_depth'][29])
        SHORT_RESULTS['Night Temperature'].append(nt)
        SHORT_RESULTS['Day 1 Growth'].append(results[i]['growth'][0])
        SHORT_RESULTS['Day 30 Growth'].append(results[i]['growth'][29])
        SHORT_RESULTS['Daphnia Consumed'].append(taway)
        SHORT_RESULTS['Sustainable Estimate'].append(taway2)
        SHORT_RESULTS['Estimated Condition Change'].append(condition)
        growths.append(results[i]['growth'][29])
        growths1.append(results[i]['growth'][0])

    return results, growths, growths1, csvheaders, sens_inputs, SHORT_RESULTS, base_val, base_set_flag


class Daph_Data:
    def __init__(self, abundance, size, year, site, month):
        self.total_daph = abundance
        self.daph_size = size
        self.d_year = year
        self.d_site = site
        self.d_month = month

class Form_Data_Packager:
    def __init__(self, form):
        self.title = form.getvalue('TabName') or 'GrowChinook Results'
        self.starting_mass = float(form.getvalue('Starting_Mass_In') or 20)
        if self.starting_mass == 0:
            self.starting_mass = 0.1
        self.total_daphnnia = float(form.getvalue('Total_Daphnia_Input_Name') or form.getvalue('TotDDef') or 123456)
        self.daphnia_size = float(form.getvalue('Daphnia Size') or form.getvalue('DaphSDef') or 123456)
        self.light = float(form.getvalue('Light') or form.getvalue('LightDef') or 123456)
        self.year = form.getvalue('Year') or '2015'
        self.month = form.getvalue('Month1') or 'June'
        self.site = form.getvalue('Site') or 'Fall Creek'
        self.max_dep = float(form.getvalue('DmaxIn') or 10000)
        self.min_dep = float(form.getvalue('DminIn') or -1)
        self.max_temp = float(form.getvalue('TmaxIn') or 10000)
        self.min_temp = float(form.getvalue('TminIn') or -1)
        if self.min_temp == self.max_temp:
            self.max_temp = self.max_temp + 1
        self.pop_site = form.getvalue('ESite') or self.site
        self.elev = float(form.getvalue('Elev') or 100000)
        if self.pop_site == 'Fall Creek':
            self.elev = max(self.elev, 690)
            self.max_dep = min(((self.elev - FC_MIN_EL) / 3.281), self.max_dep)
        elif self.pop_site == 'Lookout Point':
            self.elev = max(self.elev, 725)
            self.max_dep = min(((self.elev - LP_MIN_EL) / 3.281), self.max_dep)
        elif self.pop_site == 'Hills Creek':
            self.max_dep = min(((self.elev - HC_MIN_EL) / 3.281), self.max_dep)
        if self.max_dep <= 0:
            self.max_dep = 1
            self.dmaxday = 1
        self.daph_year = form.getvalue('DYear') or self.year
        self.daph_month = form.getvalue('DMonth') or self.month
        self.daph_site = form.getvalue('DSite') or self.site
        self.temp_year = form.getvalue('TYear') or self.year
        self.temp_month = form.getvalue('TMonth') or self.month
        self.temp_site = form.getvalue('TSite') or self.site
        if form.getvalue('CustTemp') is None:
            self.cust_temp = '{0}_T_{1}_{2}.csv'.format(self.temp_site, self.temp_month, self.temp_year)
        else:
            self.cust_temp = 'uploads/temp/{}'.format(form.getvalue('CustTemp'))

        self.light, self.total_daphnnia, self.daphnia_size = get_vals(self.light, self.total_daphnnia, self. daphnia_size, self.site, self.month, self.year)
        self.site_data = Site_Data(self.year, self.site, self.month, self.light, self.max_dep, self.min_dep)
        self.daph_data = Daph_Data(self.total_daphnnia, self.daphnia_size, self.daph_year, self.daph_site, self.daph_month)


class Adv_Sens_Form_Data_Packager:
    def __init__(self, form):
        self.title = form.getvalue('TabName') or 'GrowChinook Results'
        self.starting_mass = float(form.getvalue('Starting_Mass_In') or 20)
        if self.starting_mass == 0:
            self.starting_mass = 0.1
        self.total_daphnnia = float(form.getvalue('Total_Daphnia_Input_Name') or form.getvalue('TotDDef') or 123456)
        self.daphnia_size = float(form.getvalue('Daphnia Size') or form.getvalue('DaphSDef') or 123456)
        self.light = float(form.getvalue('Light') or form.getvalue('LightDef') or 123456)
        self.year = form.getvalue('Year') or '2015'
        self.site = form.getvalue('Site') or 'Fall Creek'
        self.max_dep = float(form.getvalue('DmaxIn') or 10000)
        self.min_dep = float(form.getvalue('DminIn') or -1)
        self.max_temp = float(form.getvalue('TmaxIn') or 10000)
        self.min_temp = float(form.getvalue('TminIn') or -1)

        if self.min_temp == self.max_temp:
            self.max_temp = self.max_temp + 1
        self.site_data = Site_Data(self.year, self.site, None, self.light, self.max_dep, self.min_dep)
        self.daph_data = Daph_Data(self.total_daphnnia, self.daphnia_size, self.year, self.site, None)


class Site_Data:
    def __init__(self, year, site, month, light, max_depth, min_depth):
        self.year = year
        self.site = site
        self.month = month
        self.light = light
        self.max_depth = max_depth
        self.min_depth = min_depth

class Batch:
    def __init__(self, site_data, starting_mass, daphnia_data, temp_max, temp_min, temp_file, elevation, PSite):
        self.site = site_data.site
        self.month = site_data.month
        self.year = site_data.year
        self.light = site_data.light
        self.daphnia_size = daphnia_data.daph_size
        self.total_daphnia = daphnia_data.total_daph
        self.temp_file = temp_file
        self.DYear = daphnia_data.d_year
        self.DMonth = daphnia_data.d_month
        self.daphnia_site = daphnia_data.d_site
        self.starting_mass = starting_mass
        self.starting_mass_initial = starting_mass
        self.depth_max = site_data.max_depth
        self.depth_min = site_data.min_depth
        self.temp_max = temp_max
        self.temp_min = temp_min
        self.dtfinal = 0
        self.ntfinal = 0
        self.depths = []
        self.elevation = elevation

        self.PSite = PSite
        self.SparamExp = []
        # Body lengths (from grey lit((())))
        self.SwimSpeed = 2
        self.params = {}
        # J/gram of O2 in respiration conversions (Elliot and Davidson 1975).
        self.O2Conv = 13560
        # lux http://sustainabilityworkshop.autodesk.com/buildings/measuring-light-levels
        self.DayLight = 39350
        self.NightLight = 0.10
        self.out = {}
        # Based of Cornell equation (g) #WetDaphWeight <- DaphWeight*(8.7/0.322)
        self.daphnia_dry_weight = (np.exp(1.468 + 2.83 * np.log(self.daphnia_size))) /\
                             1000000 #From Ghazy, others use ~10%
        self.daphnia_weight = self.daphnia_dry_weight * 8.7 / 0.322

        if elevation is None:
            self.elevation = 100000
        else:
            self.elevation = int(float(elevation)/3.281)
        self.PSite = PSite

        self.PSite = self.PSite or self.site
        self.DYear = self.DYear or self.year
        self.DMonth = self.DMonth or self.month
        self.daphnia_site = self.daphnia_site or self.site

        # From Luecke 22.7 kJ/g
        DaphEnergy = 22700
        self.prey = [1]
        # Noue and Choubert 1985 suggest Daphnia are 82.6% digestible by Rainbow Trout
        self.digestibility = [0.174]
        self.preyenergy = [DaphEnergy]

        with open('Daphnia VD.csv') as fid:
            reader = DictReader(fid)
            zooplankton_data = [r for r in reader]
        (self.daphline, self.daph_auc) = self.compute_daphniabydepth(zooplankton_data)
        # From Lookout Point and Fall Creek downstream screw trap data (R2 = 0.9933)
        self.StartingLength = (self.starting_mass / 0.000004) ** (1 / 3.1776)
        #self.StartingLength = (self.starting_mass/0.0003)**(1/2.217) #see note below

        self.temp_max = self.temp_max or 1000
        self.temp_min = self.temp_min or -1

        f = 'ChinookAppendixA.csv'
        with open(f) as fid:
            reader = DictReader(fid, quoting=QUOTE_NONNUMERIC)
            self.params = next(reader)
            if self.temp_file == "None_T_None_None.csv":
                temperature_file = '{0}_T_{1}_{2}.csv'\
                    .format(self.site, self.month, self.year)
            else:
                temperature_file = temp_file

        with open(temperature_file) as fid:
            reader = DictReader(fid)
            self.temperatures = []
            for row in reader:
                if (float(row['temp']) <= self.temp_max) and (float(row['temp']) >= self.temp_min):
                    self.temperatures.append(float(row['temp']))
                    self.depths.append(float(row['depth']))
        if self.temperatures == [] or self.depths == []:
            print("ALL DEPTHS EXCLUDED BY TEMPERATURE AND DEPTH RESTRICTIONS!!!!!!!!!")

        self.predatorenergy = self.predatorenergy(self.starting_mass)
        self.depth_from_temp = interp1d(self.temperatures, self.depths,
                                        fill_value=0, bounds_error=False)
        self.temp_from_depth = interp1d(self.depths, self.temperatures,
                                        fill_value=0, bounds_error=False)
        day_depth = 5
        night_depth = 10
        self.day_temp = self.temp_from_depth(day_depth)
        self.day_depth = 5
        self.night_temp = self.temp_from_depth(night_depth)
        self.night_depth = 10


    def compute_daphniabydepth(self, zooplankton_data):
        # get rows for site, season, depth
        if self.year == '2016':
            rows = [r for r in zooplankton_data if (r['Site'] == self.daphnia_site
                                                    and r['Month'] == self.DMonth
                                                    and r['Year'] == '2016')]
        else:
            rows = [r for r in zooplankton_data if (r['Site'] == self.daphnia_site
                                                    and r['Month'] == self.DMonth
                                                    and r['Year'] == '2015')]
        x = [float(r['Depth']) for r in rows]
        y = [float(r['Total Daphnia']) for r in rows]

        surface_count = y[np.argmin(x)]

        auc = trapz(y, x)
        y = y / auc * self.total_daphnia

        return (interp1d(x, y, bounds_error=False, fill_value=surface_count), trapz(y, x))


    # Foraging from Beauchamps paper, prey per hour
    def compute_foragingbydepth(self, StartingLength, starting_mass, surface_light,
                                daphline, daph_auc, depth):
        light = surface_light * np.exp((-self.light) * depth)
        depth = depth
        daphnia = daphline(depth) / 10000
        #reactiondistance = 3.787 * (light ** 0.4747) * ((self.daphnia_size / 10) ** 0.9463)
        lightenergy = light/51.2
        suspendedsediment = -((np.log(lightenergy) - 1.045)/(.0108))
        turbidity = .96*np.log(suspendedsediment+1) - .002
        reactiondistance = 31.64-13.31*turbidity
        if reactiondistance < .08 or np.isnan(reactiondistance):
            reactiondistance = .08
        swim_speed = self.SwimSpeed * StartingLength/10
        searchvolume = np.pi * (reactiondistance ** 2) * swim_speed
        EncounterRate = searchvolume * daphnia
        gramsER = EncounterRate * self.daphnia_weight
        return gramsER / starting_mass


    def compute_ft(self, temperature):
        CQ = self.params['CQ']
        CTL = self.params['CTL']
        CTM = self.params['CTM']
        CTO = self.params['CTO']
        CK1 = self.params['CK1']
        CK4 = self.params['CK4']
        eq = self.params['c_eq']
        if eq == 1:
            return np.exp(CQ * temperature)

        elif eq == 2:
            V = (CTM - temperature) / (CTM - CTO)
            Z = np.log(CQ) * (CTM - CTO)
            Y = np.log(CQ) * (CTM - CTO + 2)
            X = (Z ** 2 * (1 + (1 + 40 / Y) ** 0.5) ** 2) / 400
            return (V ** X) * np.exp(X * (1 - V))

        elif eq == 3:
            G1 = (1 / (CTO - CQ)) * np.log((0.98 * (1 - CK1)) / (CK1 * 0.002))
            G2 = (1 / (CTL - CTM)) * np.log((0.98 * (1 - CK4)) / (CK4 * 0.02))
            L1 = np.exp(G1 * (temperature - CQ))
            L2 = np.exp(G2 * (CTL - temperature))
            K_A = (CK1 * L1) / (1 + CK1 * (L1 - 1))
            K_B = (CK4 * L2) / (1 + CK4 * (L2 - 1))
            return K_A * K_B
        else:
            raise ValueError("Unknown consumption equation type: " + eq)


    def compute_cmax(self, W):
        CA = self.params['CA']
        CB = self.params['CB']
        return CA * (W ** CB)


    def compute_consumption(self, cmax, P, ft):
        return cmax * P * ft

    def compute_waste(self, consumption, P, temperature, prey, digestibility):
        # Units are g/g/d
        FA = self.params['FA']
        FB = self.params['FB']
        FG = self.params['FG']
        UA = self.params['UA']
        UB = self.params['UB']
        UG = self.params['UG']
        eq = self.params['egexeq']
        if eq == 1:
            egestion = FA * consumption
            excretion = UA * (consumption - egestion)
            return (egestion, excretion)
        elif eq == 2:
            egestion = FA * (temperature ** FB) * np.exp(FG * P) * consumption
            excretion = UA * (temperature ** UB) * np.exp(UG * P) * (consumption - egestion)
            return (egestion, excretion)
        elif eq == 3:
            if prey is None or digestibility is None:
                raise ValueError("Prey or digestibility not defined")
            PFF = np.inner(prey, digestibility)
            PE = FA * (temperature ** FB) * np.exp(FG * P)
            PF = ((PE - 0.1) / 0.9) * (1 - PFF) + PFF
            egestion = PF * consumption
            excretion = UA * (temperature ** UB) * np.exp(UG * P) * (consumption - egestion)
            return (egestion, excretion)
        else:
            raise ValueError("Unknown egestion/excretion equation type: " + eq)


    def compute_respiration(self, W0, temperature, egestion, consumption):
        RA = self.params['RA']
        RB = self.params['RB']
        RQ = self.params['RQ']
        RTO = self.params['RTO']
        RTM = self.params['RTM']
        RTL = self.params['RTL']
        RK1 = self.params['RK1']
        RK4 = self.params['RK4']
        ACT = self.params['ACT']
        BACT = self.params['BACT']
        SDA = self.params['SDA']
        eq = self.params['respeq']
        if eq == 1:
            if temperature > RTL:
                VEL = RK1 * W0 ** RK4
                print("SOME OF THE INCLUDED TEMPERATURES ARE LETHAL,"
                      "PLEASE MODIFY THE TEMPERATURE TO EXCLUDE TEMPERATURES OVER 25C!")
            else:
                VEL = ACT * (W0 ** RK4) * np.exp(BACT * temperature)
                FTmetabolism = np.exp(RQ * temperature)
                activity = np.exp(RTO * VEL)
        elif eq == 2:
            Vresp = (RTM - temperature) / (RTM - RTO)
            Zresp = np.log(RQ) * (RTM - RTO)
            Yresp = np.log(RQ) * (RTM - RTO + 2)
            Xresp = (((Zresp ** 2) * (1 + (1 + 40 / Yresp) ** 0.5)) ** 2) / 400
            FTmetabolism = (Vresp ** Xresp) * np.exp(Xresp * (1 - Vresp))
            activity = ACT
        else:
            raise ValueError("Unknown respiration equation type: " + eq)
        respiration = RA * (W0 ** RB) * FTmetabolism * activity
        SDAction = SDA * (consumption - egestion)
        return (respiration, SDAction)


    def predatorenergy(self, W0):
        AlphaI = self.params['AlphaI']
        AlphaII = self.params['AlphaII']
        BetaI = self.params['BetaI']
        BetaII = self.params['BetaII']
        energydensity = self.params['energydensity']
        cutoff = self.params['cutoff']
        eq = self.params['prededeq']
        if eq == 1:
            predatorenergy = energydensity
        if eq == 2:
            if W0 < cutoff:
                predatorenergy = AlphaI + (BetaI * W0)
            elif W0 >= cutoff:
                predatorenergy = AlphaII + (BetaII * W0)
        else:
            raise ValueError("Unknown predator energy density equation type: " + eq)
        return predatorenergy


    def compute_bioenergetics(self, W, temp, P, prey, digestibility):
        cmax = self.compute_cmax(W)
        ft = self.compute_ft(temp)
        consumption = self.compute_consumption(cmax, P, ft)
        (egestion, excretion) = self.compute_waste(consumption, P, temp, prey, digestibility)
        (respiration, SDAction) = self.compute_respiration(W, temp, egestion, consumption)
        return (consumption, egestion, excretion, respiration, SDAction)


    def compute_growth(self, consumption, prey, preyenergy, egestion, excretion,
                       SDAction, respiration, predatorenergy, W):
        consumptionjoules = consumption * np.inner(prey, preyenergy)
        return (consumptionjoules - ((egestion + excretion + SDAction) * np.inner(prey, preyenergy)
                                     + respiration * self.O2Conv)) / predatorenergy * W

    def best_depth(self, StartingLength, starting_mass, hours, light, depths):
        if self.depth_min > min(max(depths), self.depth_max):
            self.depth_min = min(max(depths), self.depth_max)
        if self.depth_max < max(min(depths), self.depth_min):
            self.depth_max = max(min(depths), self.depth_min)
        if self.depth_max == self.depth_min:
            self.depth_max = self.depth_max + 0.2
        depth_arr = np.arange(max(min(depths), self.depth_min), min(max(depths), self.depth_max), 0.1)
        growths = [self.growth_fn(d, StartingLength, starting_mass, hours, light, self.prey)[0]
                   for d in depth_arr]
        idx = np.argmax(growths)
        d = depth_arr[idx]
        best_growth, best_consumption = self.growth_fn(d, StartingLength, starting_mass,
                                                       hours, light, self.prey)
        return depth_arr[idx], best_growth, best_consumption


    def growth_fn(self, depth, StartingLength, starting_mass, hours, light, prey):
        temp = self.temp_from_depth(depth)
        foraging = self.compute_foragingbydepth(StartingLength, starting_mass, light,
                                                self.daphline, self.daph_auc, depth) * hours
        ft = self.compute_ft(temp)
        cmax = self.compute_cmax(starting_mass)
        P = min(foraging / cmax, 1)
        (consumption, egestion, excretion, respiration, SDAction) = \
            self.compute_bioenergetics(starting_mass, temp, P, self.prey, self.digestibility)
        day_proportion = hours / 24.0
        consumption *= day_proportion
        respiration *= day_proportion
        growth = self.compute_growth(consumption, prey, self.preyenergy, egestion, excretion,
                                     SDAction, respiration, self.predatorenergy, starting_mass)
        return (growth, consumption)


    def Run_Batch(self):
        daylength = {'March':11.83, 'April':13.4, 'May':14.73, 'June':15.42,
                     'July':15.12, 'August':13.97, 'September':12.45}
        # March 11:50 (11.83), April 13:24 (13.4), May 14:44 (14.73), June 15:25 (15.42),
        # July 15:07 (15.12), August 13:58 (13.97), September 12:27 (12.45)
        ndays = 30
        day_hours = daylength[self.month]
        night_hours = 24 - day_hours

        self.out = {'Year':[], 'Site':[], 'Month':[], 'Fish Starting Mass':[],
                    'Light Extinction Coefficient':[], 'Daphnia Size':[], 'Daphnia Density':[],
                    'StartingLength':[], 'StartingMass':[], 'growth':[], 'day_depth':[],
                    'night_depth':[]}
        condition1 = float(100*self.starting_mass*((self.StartingLength/10)**(-3.0)))
        for d in range(ndays):
            (day_depth, day_growth, day_consumption) =\
                self.best_depth(self.StartingLength, self.starting_mass,
                                day_hours, self.DayLight, self.depths)
            (night_depth, night_growth, night_consumption) =\
                self.best_depth(self.StartingLength, self.starting_mass,
                                night_hours, self.NightLight, self.depths)
            self.day_temp = self.temp_from_depth(day_depth)
            self.night_temp = self.temp_from_depth(night_depth)
            growth = day_growth + night_growth
            dailyconsume = ((day_consumption + night_consumption)*self.starting_mass)\
                           /self.daphnia_weight
            self.starting_mass += growth
            if growth > 0:
                # From LP and FC screw trap data (R2 = 0.9933)
                self.StartingLength = (self.starting_mass / 0.000004) ** (1 / 3.1776)
                #self.StartingLength = (self.starting_mass / 0.0003) ** (1 / 2.217)
                #weight to fork length (MacFarlane and Norton 2008)
                #Checked fish lengths against this and by end of summer
                # fish weigh much less than they 'should' based on their length

            self.out['Year'].append(self.year)
            self.out['Site'].append(self.site)
            self.out['Month'].append(self.month)
            self.out['Fish Starting Mass'].append(self.starting_mass)
            self.out['Light Extinction Coefficient'].append(self.light)
            self.out['Daphnia Size'].append(self.daphnia_size)
            self.out['Daphnia Density'].append(self.total_daphnia)
            self.out['day_depth'].append(day_depth)
            self.out['night_depth'].append(night_depth)
            self.out['growth'].append(growth)
            self.out['StartingMass'].append(self.starting_mass)
            self.out['StartingLength'].append(self.StartingLength)
            dtfinal = self.day_temp
            ntfinal = self.night_temp

        ele = self.elevation-int(day_depth)
        daph = self.daphline(day_depth)
        PopEst = get_sustain_est(ele, daph, dailyconsume, self.PSite)
        condition = float(100*(self.starting_mass-self.starting_mass_initial)*((self.StartingLength/10)**(-3.0)))
        return self.out, dailyconsume, condition, condition1, dtfinal, ntfinal, PopEst

