#!/usr/bin/python
import pylab,glob,os,time
from numpy import *
from scipy.interpolate import interp1d
from scipy.integrate import trapz
from scipy.optimize import minimize_scalar
from csv import DictReader, QUOTE_NONNUMERIC
from collections import defaultdict
from matplotlib import pyplot
from datetime import datetime, timedelta

def Scruffy(): #Scruffy's the janitor. Kills any output files older than one hour
    for file in glob.glob("output*"):
        st=os.stat(file)    
        age=st.st_mtime
        if (time.time() - age) >= 3600:
            os.remove(file)

def GetVals(Light,Total_Daphnia,DaphSize,Site,Month,Year):
    FallCreeklength = dict([('March',31),('April',30),('May',31),('June',30),('July',31),('August',31),('September',30)])
    HillsCreeklength = dict([('March',31),('April',30),('May',31),('June',30),('July',31),('August',31),('September',30)])
    LookoutPointlength = dict([('March',31),('April',30),('May',31),('June',30),('July',31),('August',31),('September',30)])
#k represents the light extinction coefficient
    FCk16 = dict([('April',0.758),('May',0.466),('June',0.435),('July',0.451),('August',0.444),('September',0.406)])
    HCk16 = dict([('April',0.399),('May',0.321),('June',0.440),('July',0.257),('August',0.384),('September',0.340)])
    LPk16 = dict([('April',0.514),('May',0.373),('June',0.368),('July',0.311),('August',0.389),('September',0.343)])
    FCk15 = dict([('March',0.834),('April',0.596),('May',0.58),('June',0.72),('July',0.521),('August',0.509)])
    HCk15 = dict([('March',0.583),('April',0.503),('May',0.467),('June',0.441),('July',0.32),('August',0.368)])
    LPk15 = dict([('March',0.532),('April',0.565),('May',0.373),('June',0.374),('July',0.396),('August',0.39)])
    FCk14 = dict([('June',0.404),('July',0.274),('August',0.295)])
    HCk14 = dict([('June',0.298),('July',0.274),('August',0.274)])
    LPk14 = dict([('June',0.315),('July',0.271),('August',0.282)])
    BRk14 = dict([('July',0.254)])
    FCk13 = dict([('August',0.487)])
    HCk13 = dict([('August',0.291)])
    BRk13 = dict([('August',0.263)])
#Daphnia totals weighted by subsample - only from C and Z sites #July 2013 and July 2014 are not currently available
    FCd16 = dict([('April', 367),('May',22328),('June',48240),('July',8801),('August',5378),('September',3626)])
    HCd16 = dict([('April',163),('May',7456),('June',88658),('July',9045),('August',13527),('September',13853)])
    LPd16 = dict([('April',20),('May',448),('June',9290),('July',11693),('August',6926),('September',1854)])
    FCd15 = dict([('March', 815), ('April', 17357), ('May', 24446), ('June',3993), ('July', 2363),('August', 407)])
    HCd15 = dict([('March', 204), ('April', 453), ('May', 11408), ('June', 20535), ('July', 9126),('August', 3178)])
    LPd15 = dict([('March', 61), ('April', 127), ('May', 14016), ('June', 44981), ('July', 5949),('August', 581)])
    BRd15 = dict([('March', 163), ('April', 774), ('May', 19068), ('June', 20861), ('July', 7578),('August', 7496)])
    FCd14 = dict([('June', 25280), ('July', 0), ('August', 7752)])
    HCd14 = dict([('June', 6040), ('July', 0), ('August', 2249)])
    LPd14 = dict([('June', 16863), ('July', 0), ('August', 1061)])
    FCd13 = dict([('June', 18416), ('July', 0), ('August', 4563)])
    HCd13 = dict([('June', 127772), ('July', 0), ('August', 18559)])
    BRd13 = dict([('June', 68449), ('July', 0), ('August', 41233)])
#Weighted for proportion D. mendotae, D. pulex, and D. rosea/ambigua averaged across available years
    FCsize = dict([('March',1.207),('April',0.90375),('May',1.073),('June',1.262),('July',1.485),('August',1.633)])
    HCsize = dict([('March',1.238),('April',1.152),('May',1.058),('June',1.232),('July',1.687),('August',2.005)])
    LPsize = dict([('March',1.457),('April',0.745),('May',0.871),('June',1.237),('July',1.642),('August',2.033)])
    BRsize = dict([('March',0.628),('April',0.780),('May',0.827),('June',1.321),('July',1.377),('August',1.282)])

    if Light == None and Site =='Fall Creek' and Year == '2016':
        Light = FCk16[Month]
    elif Light == None and Site =='Hills Creek' and Year == '2016':
        Light = HCk16[Month]
    elif Light == None and Site  == 'Lookout Point' and Year == '2016':
        Light = LPk16[Month]
    elif Light == None and Site =='Fall Creek' and Year == '2015':
        Light = FCk15[Month]
    elif Light == None and Site =='Hills Creek' and Year == '2015':
        Light = HCk15[Month]
    elif Light == None and Site  == 'Lookout Point' and Year == '2015':
        Light = LPk15[Month]
    elif Light == None and Site  =='Fall Creek' and Year == '2014':
        Light = FCk14[Month]
    elif Light == None and Site =='Hills Creek' and Year == '2014':
        Light = HCk14[Month]
    elif Light == None and Site  == 'Lookout Point' and Year == '2014':
        Light = LPk14[Month]

    if Total_Daphnia == None and Site =='Fall Creek' and Year == '2016':
        Total_Daphnia = FCd16[Month]
    elif Total_Daphnia == None and Site =='Hills Creek' and Year == '2016':
        Total_Daphnia = HCd16[Month]
    elif Total_Daphnia == None and Site  == 'Lookout Point' and Year == '2016':
        Total_Daphnia = LPd16[Month]
    elif Total_Daphnia == None and Site =='Fall Creek' and Year == '2015':
        Total_Daphnia = FCd15[Month]
    elif Total_Daphnia == None and Site =='Hills Creek' and Year == '2015':
        Total_Daphnia = HCd15[Month]
    elif Total_Daphnia == None and Site  == 'Lookout Point' and Year == '2015':
        Total_Daphnia = LPd15[Month]
    elif Total_Daphnia == None and Site  =='Fall Creek' and Year == '2014':
        Total_Daphnia = FCd14[Month]
    elif Total_Daphnia == None and Site =='Hills Creek' and Year == '2014':
        Total_Daphnia = HCd14[Month]
    elif Total_Daphnia == None and Site  == 'Lookout Point' and Year == '2014':
        Total_Daphnia = LPd14[Month]

    if DaphSize == None and Site  =='Fall Creek':
        DaphSize = FCsize[Month]
    elif DaphSize == None and Site  =='Hills Creek':
        DaphSize = HCsize[Month]
    elif DaphSize == None and Site  == 'Lookout Point':
        DaphSize = LPsize[Month]
    return Light,Total_Daphnia,DaphSize

def Sensitivity_Expand(Sparam_Range, Sparam_Exp):
    step_size = Sparam_Range/500
    Sparam_Range = (Sparam_Range/100)*-1
    for i in range(0,11):
        Sparam_Exp.append(Sparam_Range)
        Sparam_Range = Sparam_Range + step_size
    return Sparam_Exp


class Batch:
    def __init__(self, Site, Month, Year, Light, DaphSize, TotalDaphnia, StartingMass, Dmax, Dmin,Tmax,Tmin,TempCurve,DYear,DMonth,DSite):
        self.Site = Site
        self.Month = Month
        self.Year = Year
        self.Light = Light
        self.DaphSize = DaphSize
        self.TotalDaphnia = TotalDaphnia
        self.TempCurve = TempCurve
        self.DYear = DYear
        self.DMonth = DMonth
        self.DSite = DSite
        self.StartingMass = StartingMass
        self.SMass = StartingMass
        self.Dmax = Dmax
        self.Dmin = Dmin
        self.Tmax = Tmax
        self.Tmin = Tmin
        self.dtfinal = 0
        self.ntfinal = 0
        self.Depths = []
        self.SparamExp = []
        self.SwimSpeed = 2 #Body lengths (from grey lit((())))
        self.params = {}
        self.O2Conv = 13560  # J/gram of O2 in respiration conversions (Elliot and Davidson 1975).
        self.DayLight = 39350  # lux http://sustainabilityworkshop.autodesk.com/buildings/measuring-light-levels
        self.NightLight = 0.10
        self.out = {}
        self.DaphWeightdry = (exp(1.468 + 2.83 * log(self.DaphSize))) / 1000000  # Based of Cornell equation (g) #WetDaphWeight <- DaphWeight*(8.7/0.322) #From Ghazy, others use ~10%
        self.DaphWeight = self.DaphWeightdry * 8.7 / 0.322
        
        if self.DYear == None:
            self.DYear = self.Year
        if self.DMonth == None:
            self.DMonth = self.Month
        if self.DSite == None:
            self.DSite = self.Site

        DaphEnergy = 22700  # From Luecke 22.7 kJ/g
        self.prey = [1]
        self.digestibility = [0.174]  # Noue and Choubert 1985 suggest Daphnia are 82.6% digestible by Rainbow Trout
        self.preyenergy = [DaphEnergy]

        with open('Daphnia VD 2015.csv') as fid:
            reader = DictReader(fid)
            zooplankton_data = [r for r in reader]
        (self.daphline, self.daph_auc) = self.compute_daphniabydepth(zooplankton_data)
        self.StartingLength = 49.54 * (self.StartingMass ** (0.3126))
        #self.StartingLength = (self.StartingMass/0.0003)**(1/2.217) #see note below
        
        if self.Tmax == None:
            self.Tmax = 1000
        if self.Tmin == None:
            self.Tmin = -1        
        

        f = 'ChinookAppendixA.csv'
        with open(f) as fid:
            reader = DictReader(fid, quoting=QUOTE_NONNUMERIC)
            self.params = next(reader)
            if self.TempCurve == "None_smoothed_None_None.csv":
                temperature_file = '{0}_smoothed_{1}_{2}.csv'.format(self.Site, self.Month, self.Year)
            else:
                temperature_file = TempCurve
 
        
        with open(temperature_file) as fid:
            reader = DictReader(fid)
            self.temperatures = []
            for row in reader:
                if ((float(row['temp']) <= self.Tmax) and (float(row['temp']) >= self.Tmin)):
                    self.temperatures.append(float(row['temp']))
                    self.Depths.append(float(row['depth']))

        self.predatorenergy = self.predatorenergy(self.StartingMass)
        self.depth_from_temp = interp1d(self.temperatures, self.Depths, fill_value=0, bounds_error=False)
        self.temp_from_depth = interp1d(self.Depths, self.temperatures, fill_value=0, bounds_error=False)
        day_depth = 5
        day_temp = None
        night_depth = 10
        night_temp = None
        self.day_temp = day_temp or self.temp_from_depth(day_depth)
        self.day_depth = day_depth or self.depth_from_temp(day_temp)
        self.night_temp = night_temp or self.temp_from_depth(night_depth)
        self.night_depth = night_depth or self.depth_from_temp(night_temp)




    def compute_daphniabydepth(self, zooplankton_data):
        # get rows for site, season, depth
        rows = [r for r in zooplankton_data if (r['Site'] == self.DSite
                                                and r['Month'] == self.DMonth
                                                and r['Year'] == self.DYear)]
        x = [float(r['Depth']) for r in rows]
        y = [float(r['Total Daphnia']) for r in rows]

        surface_count = y[argmin(x)]

        auc = trapz(y, x)
        y = y / auc * self.TotalDaphnia

        return (interp1d(x, y, bounds_error=False, fill_value=surface_count), trapz(y, x))


    # Foraging from Beauchamps paper, prey per hour
    def compute_foragingbydepth(self, StartingLength, StartingMass, surface_light, daphline, daph_auc, depth):
        light = surface_light * exp((-self.Light) * depth)
        depth = depth
        daphnia = daphline(depth) / 10000
        reactiondistance = 3.787 * (light ** 0.4747) * ((self.DaphSize / 10) ** 0.9463)
        swim_speed = self.SwimSpeed * StartingLength/10
        searchvolume = pi * (reactiondistance ** 2) * swim_speed
        EncounterRate = searchvolume * daphnia
        gramsER = EncounterRate * self.DaphWeight
        return gramsER / StartingMass


    def compute_ft(self, temperature):
        CQ = self.params['CQ']
        CTL = self.params['CTL']
        CTM = self.params['CTM']
        CTO = self.params['CTO']
        CK1 = self.params['CK1']
        CK4 = self.params['CK4']
        eq = self.params['c_eq']
        if eq == 1:
            return exp(CQ * temperature)

        elif eq == 2:
            V = (CTM - temperature) / (CTM - CTO)
            Z = log(CQ) * (CTM - CTO)
            Y = log(CQ) * (CTM - CTO + 2)
            X = (Z ** 2 * (1 + (1 + 40 / Y) ** 0.5) ** 2) / 400
            return (V ** X) * exp(X * (1 - V))

        elif eq == 3:
            G1 = (1 / (CTO - CQ)) * log((0.98 * (1 - CK1)) / (CK1 * 0.002))
            G2 = (1 / (CTL - CTM)) * log((0.98 * (1 - CK4)) / (CK4 * 0.02))
            L1 = exp(G1 * (temperature - CQ))
            L2 = exp(G2 * (CTL - temperature))
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
            egestion = FA * (temperature ** FB) * exp(FG * P) * consumption
            excretion = UA * (temperature ** UB) * exp(UG * P) * (consumption - egestion)
            return (egestion, excretion)
        elif eq == 3:
            if prey is None or digestibility is None:
                raise ValueError("Prey or digestibility not defined")
            PFF = inner(prey, digestibility)
            PE = FA * (temperature ** FB) * exp(FG * P)
            PF = ((PE - 0.1) / 0.9) * (1 - PFF) + PFF
            egestion = PF * consumption
            excretion = UA * (temperature ** UB) * exp(UG * P) * (consumption - egestion)
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
            else:
                VEL = ACT * (W0 ** RK4) * exp(BACT * temperature)
                FTmetabolism = exp(RQ * temperature)
                activity = exp(RTO * VEL)
        elif eq == 2:
            Vresp = (RTM - temperature) / (RTM - RTO)
            Zresp = log(RQ) * (RTM - RTO)
            Yresp = log(RQ) * (RTM - RTO + 2)
            Xresp = (((Zresp ** 2) * (1 + (1 + 40 / Yresp) ** 0.5)) ** 2) / 400
            FTmetabolism = (Vresp ** Xresp) * exp(Xresp * (1 - Vresp))
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


    def compute_growth(self, consumption, prey, preyenergy, egestion, excretion, SDAction, respiration, predatorenergy, W):
        consumptionjoules = consumption * inner(prey, preyenergy)
        return (consumptionjoules - ((egestion + excretion + SDAction) * inner(prey, preyenergy) + respiration * self.O2Conv)) / predatorenergy * W

    def best_depth(self, StartingLength,StartingMass,hours,light, depths):
        if self.Dmin > min(max(depths),self.Dmax):
            self.Dmin = min(max(depths),self.Dmax)
        if self.Dmax < max(min(depths),self.Dmin):
            self.Dmax = max(min(depths),self.Dmin)
        if self.Dmax == self.Dmin:
            self.Dmax = self.Dmax + 0.2
        depth_arr = arange(max(min(depths),self.Dmin),min(max(depths),self.Dmax),0.1)
        growths = [self.growth_fn(d,StartingLength,StartingMass,hours,light,self.prey)[0] for d in depth_arr]
        idx = argmax(growths)
        d = depth_arr[idx]
        best_growth,best_consumption = self.growth_fn(d,StartingLength,StartingMass,hours,light,self.prey)
        return depth_arr[idx], best_growth, best_consumption

    def plot_growth():
        depth_arr = arange(min(depths),max(depths),0.1)
        gs_d = [growth_fn(d,self.out['StartingLength'][0],self.out['StartingMass'][0],day_hours,DayLight,self.prey) for d in depth_arr]
        gs_n = [growth_fn(d, self.out['StartingLength'][0], self.out['StartingMass'][0], night_hours, NightLight,self.prey) for d in depth_arr]
        pylab.plot(depth_arr,gs_d)
        pylab.plot(depth_arr,gs_n)

    def growth_fn(self, depth, StartingLength, StartingMass, hours, light, prey):
        temp = self.temp_from_depth(depth)
        foraging = self.compute_foragingbydepth(StartingLength, StartingMass, light, self.daphline, self.daph_auc, depth) * hours
        ft = self.compute_ft(temp)
        cmax = self.compute_cmax(StartingMass)
        P = min(foraging / cmax, 1)
        (consumption, egestion, excretion, respiration, SDAction) = self.compute_bioenergetics(StartingMass, temp, P, self.prey, self.digestibility)
        day_proportion = hours / 24.0
        consumption *= day_proportion
        respiration *= day_proportion
        growth = self.compute_growth(consumption, prey, self.preyenergy, egestion, excretion, SDAction,respiration, self.predatorenergy, StartingMass)
        return (growth,consumption)


    def Run_Batch(self):
        daylength = dict([('March',11.83),('April',13.4),('May',14.73),('June',15.42),('July',15.12),('August',13.97),('September',12.45)])
        # March 11:50 (11.83), April 13:24 (13.4), May 14:44 (14.73), June 15:25 (15.42), July 15:07 (15.12), August 13:58 (13.97), September 12:27 (12.45)
        ndays = 30
        day_hours = daylength[self.Month]
        night_hours = 24 - day_hours
        day_length = day_hours / 24.0
        night_length = night_hours / 24.0

        TotalConsumption = 0

        output = []
        finalLW = []

        self.out = {'Year':[],'Site':[],'Month':[],'Fish Starting Mass':[],'Light Extinction Coefficient':[],'Daphnia Size':[],'Daphnia Density':[],'StartingLength':[],'StartingMass':[],'growth':[],'day_depth':[],'night_depth':[]}
        condition1 = float(100*self.StartingMass*((self.StartingLength/10)**(-3.0)))
        for d in range(ndays):
            (day_depth, day_growth, day_consumption) = self.best_depth(self.StartingLength, self.StartingMass, day_hours, self.DayLight, self.Depths)
            (night_depth, night_growth, night_consumption) = self.best_depth(self.StartingLength, self.StartingMass, night_hours, self.NightLight, self.Depths)

            growth = day_growth + night_growth
            dailyconsume = ((day_consumption + night_consumption)*self.StartingMass)/self.DaphWeight
            self.StartingMass += growth
            if growth > 0:
                self.StartingLength = 49.54 * (self.StartingMass ** (0.3126))
                #self.StartingLength = (self.StartingMass / 0.0003) ** (1 / 2.217)  # weight to fork length (MacFarlane and Norton 2008)
                    #Checked fish lengths against this and by end of summer fish weigh much less than they 'should' based on their length
            
            self.out['Year'].append(self.Year)
            self.out['Site'].append(self.Site)
            self.out['Month'].append(self.Month)
            self.out['Fish Starting Mass'].append(self.StartingMass)
            self.out['Light Extinction Coefficient'].append(self.Light)
            self.out['Daphnia Size'].append(self.DaphSize)
            self.out['Daphnia Density'].append(self.TotalDaphnia)
            self.out['day_depth'].append(day_depth)
            self.out['night_depth'].append(night_depth)
            self.out['growth'].append(growth)
            self.out['StartingMass'].append(self.StartingMass)
            self.out['StartingLength'].append(self.StartingLength)
            dtfinal = self.day_temp
            ntfinal = self.night_temp

        condition = float(100*(self.StartingMass-self.SMass)*((self.StartingLength/10)**(-3.0)))
        return (self.out, dailyconsume,condition,condition1,dtfinal,ntfinal)

