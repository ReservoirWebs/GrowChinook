import pylab
from numpy import *
from scipy.interpolate import interp1d
from scipy.integrate import trapz
from scipy.optimize import minimize_scalar
from csv import DictReader, QUOTE_NONNUMERIC
from collections import defaultdict
from matplotlib import pyplot



class Batch:
    def __init__(self, Site, Month, Year, Light, DaphSize, TotalDaphnia, StartingMass, Dmax, Dmin):
        self.Site = Site
        self.Month = Month
        self.Year = Year
        self.Light = Light
        self.DaphSize = DaphSize
        self.TotalDaphnia = TotalDaphnia
        self.StartingMass = StartingMass
        self.Dmax = Dmax
        self.Dmin = Dmin
        self.Depths = []
        self.SparamExp = []
        self.SwimSpeed = 2 #Body lengths (from grey lit((())))
        self.params = {}
        self.O2Conv = 13560  # J/gram of O2 in respiration conversions (Elliot and Davidson 1975).
        self.DayLight = 10000  # lux http://sustainabilityworkshop.autodesk.com/buildings/measuring-light-levels
        self.NightLight = 0.11
        self.out = {}

        FallCreeklength = dict([('March',31),('April',30),('May',31),('June',30),('July',31),('August',31),('September',30)])
        HillsCreeklength = dict([('March',31),('April',30),('May',31),('June',30),('July',31),('August',31),('September',30)])
        LookoutPointlength = dict([('March',31),('April',30),('May',31),('June',30),('July',31),('August',31),('September',30)])

        FCk = dict([('March',0.834),('April',0.596),('May',0.58),('June',0.72),('July',0.521),('August',0.509)])
        HCk = dict([('March',0.583),('April',0.503),('May',0.467),('June',0.441),('July',0.32),('August',0.368)])
        LPk = dict([('March',0.532),('April',0.565),('May',0.373),('June',0.374),('July',0.396),('August',0.39)])
        FCk14 = dict([('June',0.404),('July',0.274),('August',0.295)])
        HCk14 = dict([('June',0.298),('July',0.274),('August',0.274)])
        LPk14 = dict([('June',0.315),('July',0.271),('August',0.282)])
        BRk14 = dict([('July',0.254)])
        FCk13 = dict([('August',0.487)])
        HCk13 = dict([('August',0.291)])
        BRk13 = dict([('August',0.263)])
        #Daphnia totals considering max densities from ALL Sites
        #Daphnia totals only from C and Z sites
        FCd = dict([('March',62.83),('April',722.57),('May',1093.27),('June',502.65),('July',201.06),('August',194.78)])
        HCd = dict([('March',12.57),('April',17.48),('May',578.05),('June',5931.33),('July',414.69),('August',339.29)])
        LPd = dict([('March',3.14),('April',4.91),('May',578.05),('June',2111.15),('July',703.72),('August',1382.30)])
        #July 2013 and July 2014 is average of June and August from same year
        FCd14 = dict([('June',450.13),('July',0),('August',40.72)])
        HCd14 = dict([('June',262.39),('July',0),('August',13.70)])
        LPd14 = dict([('June',531.56),('July',0),('August',93.87)])
        FCd13 = dict([('June',816.81),('July',0),('August',1269.20)])
        HCd13 = dict([('June',6584.78),('July',0),('August',845.09)])
        BRd13 = dict([('June',12767.43),('July',0),('August',1671.33)])
        #Weighted for proportion D. mendotae vs. D. pulex
        FCsize = dict([('March',1.207),('April',1.248),('May',1.139),('June',1.305),('July',1.514),('August',1.145)])
        HCsize = dict([('March',1.455),('April',1.077),('May',1.053),('June',1.045),('July',1.769),('August',1.516)])
        LPsize = dict([('March',1.457),('April',0.957),('May',1.064),('June',1.247),('July',1.664),('August',2.002)])
        BRsize = dict([('March',0.628),('June',1.497),('August',1.252)])
        #July 2013 and July 2014 is average of June and August from same year
        FCsize = dict([('March',1.207),('April',1.248),('May',1.139),('June',1.305),('July',1.514),('August',1.145)])
        HCsize = dict([('March',1.455),('April',1.077),('May',1.053),('June',1.045),('July',1.769),('August',1.516)])
        LPsize = dict([('March',1.457),('April',0.957),('May',1.064),('June',1.247),('July',1.664),('August',2.002)])
        BRsize = dict([('March',0.628),('June',1.497),('August',1.252)])

        if self.Light == None and self.Site =='Fall Creek' and self.Year == '2015':
            self.Light = FCk[Month]
        elif self.Light == None and self.Site =='Hills Creek' and self.Year == '2015':
            self.Light = HCk[Month]
        elif self.Light == None and self.Site  == 'Lookout Point' and self.Year == '2015':
            self.Light = LPk[Month]
        elif self.Light == None and self.Site  =='Fall Creek' and self.Year == '2014':
            self.Light = FCk14[Month]
        elif self.Light == None and self.Site =='Hills Creek' and self.Year == '2014':
            self.Light = HCk14[Month]
        elif self.Light == None and self.Site  == 'Lookout Point' and self.Year == '2014':
            self.Light = LPk14[Month]

        if self.TotalDaphnia == None and self.Site  =='Fall Creek':
            self.TotalDaphnia = FCd[Month]
        elif self.TotalDaphnia == None and self.Site =='Hills Creek':
            self.TotalDaphnia = HCd[Month]
        elif self.TotalDaphnia == None and self.Site  == 'Lookout Point':
            self.TotalDaphnia = LPd[Month]

        if self.DaphSize == None and self.Site  =='Fall Creek':
            self.DaphSize = FCsize[Month]
        elif self.DaphSize == None and self.Site  =='Hills Creek':
            self.DaphSize = HCsize[Month]
        elif self.DaphSize == None and self.Site  == 'Lookout Point':
            self.DaphSize = LPsize[Month]

        self.DaphWeightdry = (exp(1.468 + 2.83 * log(self.DaphSize))) / 1000000  # Based of Cornell equation (g) #WetDaphWeight <- DaphWeight*(8.7/0.322) #From Ghazy, others use ~10%
        self.DaphWeight = self.DaphWeightdry * 8.7 / 0.322

        DaphEnergy = 22700  # From Luecke 22.7 kJ/g
        self.prey = [1]
        self.digestibility = [0.174]  # Noue and Choubert 1985 suggest Daphnia are 82.6% digestible by Rainbow Trout
        self.preyenergy = [DaphEnergy]

        with open('Daphnia VD 2015.csv') as fid:
            reader = DictReader(fid)
            zooplankton_data = [r for r in reader]
        (self.daphline, self.daph_auc) = self.compute_daphniabydepth(zooplankton_data)

        self.StartingLength = (self.StartingMass/0.0003)**(1/2.217)


        f = 'ChinookAppendixA.csv'
        with open(f) as fid:
            reader = DictReader(fid, quoting=QUOTE_NONNUMERIC)
            self.params = next(reader)
            temperature_file = '{0}_smoothed_{1}_{2}.csv'.format(self.Site, self.Month, self.Year)

        with open(temperature_file) as fid:
            reader = DictReader(fid)
            self.temperatures = []
            for row in reader:
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
        rows = [r for r in zooplankton_data if (r['Site'] == self.Site
                                                # and r['Season'] == Season
                                                and r['Month'] == self.Month
                                                and r['Year'] == self.Year)]
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
        swim_speed = self.SwimSpeed * StartingLength
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
        growth = self.compute_growth(consumption, prey, self.preyenergy, egestion, excretion, SDAction,
                                     respiration, self.predatorenergy, StartingMass)
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

        self.out = {'StartingLength':[],'StartingMass':[],'growth':[],'day_depth':[],'night_depth':[]}

        for d in range(ndays):
            (day_depth, day_growth, day_consumption) = self.best_depth(self.StartingLength, self.StartingMass, day_hours, self.DayLight, self.Depths)
            (night_depth, night_growth, night_consumption) = self.best_depth(self.StartingLength, self.StartingMass, night_hours, self.NightLight, self.Depths)

            growth = day_growth + night_growth
            dailyconsume = ((day_consumption + night_consumption)*self.StartingMass)/self.DaphWeight
            self.StartingMass += growth
            if growth > 0:
                self.StartingLength = (self.StartingMass / 0.0003) ** (1 / 2.217)  # weight to fork length (MacFarlane and Norton 2008)
                #Checked fish lengths against this and by end of summer fish weigh much less than they 'should' based on their length

            self.out['day_depth'].append(day_depth)
            self.out['night_depth'].append(night_depth)
            self.out['growth'].append(growth)
            self.out['StartingMass'].append(self.StartingMass)
            self.out['StartingLength'].append(self.StartingLength)


        return (self.out, dailyconsume)

