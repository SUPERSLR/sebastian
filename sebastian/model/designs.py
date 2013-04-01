#!/usr/bin/python
# David Newell
# sebastian/model/designs.py
# Calculate cost using given functions
# These functions should return a dictionary. The 'cost' entry is
# used to determine the path used, but other entries may be passed along
# for other uses.

# Calculate cost for given length, elevation, and parameters
# l - distance between points (meters)
# elev - average elevation between points (meters)
# params - local port parameters
def NTC_CS(l,elev,params):
    # Set parameters
    # sea level rise height
    r = float(params['sea_level_rise'])
    # freeboard height
    f = float(params['freeboard'])
    # design wave height
    w_d = float(params['design_wave_height'])
    # storm surge height
    h_s = float(params['storm_surge'])
    # mean high-high tide height
    t_h = float(params['mean_high_high_tide'])
    # mean low-low tide height
    t_l = float(params['mean_low_low_tide'])
    # dike flat top width
    a_d = float(params['dike_flat_top'])
    # foundation height
    h_f = float(params['foundation_height'])
    # toe height
    h_t = float(params['toe_height'])
    # outer toe slope
    m_to = float(params['outer_toe_slope'])
    # outer dike slope
    m_do = float(params['outer_dike_slope'])
    # inner dike slope
    m_di = float(params['inner_dike_slope'])

    # Protection Height
    ph = r + f + w_d + h_s + t_h

    # Dike height equals (protection height - elevation)
    z = ph - elev

    # Calculate constants
    a = 1 / (2 * m_do) + 1 / (2 * m_di)
    b = a_d + h_f * a
    c = h_t**2 * (1 / (2 * m_to) - 1 / (2 * m_do)) + h_f * a_d + 2 * h_f * h_t * a

    # Calculate Cost
    cost = l * (c + b * z + a * z**2)

    # Return Cost
    return {'cost' : cost}


# Ben & Merel's attempt to save the world
def pieceByPiece(length, elev, params):
    # Set parameters
    # sea level rise height
    slr = float(params['sea_level_rise'])
    # freeboard height
    freeboard = float(params['freeboard'])
    # design wave height
    wave = float(params['design_wave_height'])
    # storm surge height
    surge = float(params['storm_surge'])
    # mean high-high tide height
    highTide = float(params['mean_high_high_tide'])
    # mean low-low tide height
    lowTide = float(params['mean_low_low_tide'])
    # dike flat top width
    dikeTop = float(params['dike_flat_top'])
    # foundation height
    foundHt = float(params['foundation_height'])
    # toe height
    toeHt = float(params['toe_height'])
    # outer toe slope
    toeOutSlope = float(params['outer_toe_slope'])
    # inner toe slope
    toeInSlope = float(params['inner_toe_slope'])
    # outer core slope
    coreOutSlope = float(params['outer_core_slope'])
    # inner core slope
    coreInSlope = float(params['inner_core_slope'])
    # core flat top
    coreTop = float(params['core_flat_top'])
    # core height
    coreHt = float(params['core_height'])
    # outer dike slope
    dikeOutSlope = float(params['outer_dike_slope'])
    # inner dike slope
    dikeInSlope = float(params['inner_dike_slope'])
    # armor depth
    armorDepth = float(params['armor_depth'])

    # triangular toe
    toeBase = toeOutSlope * toeHt + toeInSlope * toeHt
    toeVolume = 0.5 * toeBase * toeHt * length

    # trapezoidal core
    coreBase = coreInSlope * coreHt + coreOutSlope * coreHt + coreTop
    coreVolume = 0.5 * (coreBase + coreTop) * coreHt * length

    # trapezoidal shape
    dikeHt = highTide + surge + wave + freeboard + slr - elev
    dikeBase = dikeOutSlope * dikeHt + dikeInSlope * dikeHt + dikeTop
    # volume of trapezoid, but subtract out toe and core volumes
    dikeVolume = 0.5 * (dikeBase + dikeTop) * dikeHt * length - toeVolume - coreVolume

    # foundation just a rectangle under the base
    foundBase = toeBase + dikeBase
    foundVolume = foundBase * foundHt * length

    # armoring - find surface area of dike, then add a layer of armoring
    outerSurfaceArea = ((dikeOutSlope * dikeHt) ** 2.0 + dikeHt ** 2.0) ** 0.5 * length
    innerSurfaceArea = ((dikeInSlope * dikeHt) ** 2.0 + dikeHt ** 2.0) ** 0.5 * length
    surfaceArea = outerSurfaceArea + innerSurfaceArea
    armorVolume = surfaceArea * armorDepth

    if dikeVolume < 0.0:
        # This implies that the dike height is very low and the elevation is very high.
        # Assume these areas don't really need a dike (over land). Negative numbers break
        # the routing algorithm, so set everything to 0.
        dikeVolume = 0.0
        coreVolume = 0.0
        toeVolume = 0.0
        armorVolume = 0.0
        foundVolume = 0.0
    # for purposes of the algorithm, the dike volume can proxy for the cost
    return {   'toeVol': toeVolume,
                        'coreVol' : coreVolume,
                        'dikeVol' : dikeVolume,
                        'foundVol' : foundVolume,
                        'armorVol' : armorVolume,
                'cost' : dikeVolume + coreVolume + toeVolume + foundVolume + armorVolume
            }



# David Newell's SUPERSLR Minimum-Criteria Dike Design
def SMCDD(length, elev, params):
    # Set parameters
    # sea level rise height
    slr = float(params['sea_level_rise'])
    # freeboard height
    freeboard = float(params['freeboard'])
    # design wave height
    wave = float(params['design_wave_height'])
    # storm surge height
    surge = float(params['storm_surge'])
    # mean high-high tide height
    highTide = float(params['mean_high_high_tide'])
    # mean low-low tide height
    lowTide = float(params['mean_low_low_tide'])
    # dike flat top width
    dikeTop = float(params['dike_flat_top'])
    # foundation height
    foundHt = float(params['foundation_height'])
    # toe height
    toeHt = float(params['toe_height'])
    # outer toe slope
    toeOutSlope = float(params['outer_toe_slope'])
    # inner toe slope
    toeInSlope = float(params['inner_toe_slope'])
    # outer core slope
    coreOutSlope = float(params['outer_core_slope'])
    # inner core slope
    coreInSlope = float(params['inner_core_slope'])
    # core flat top
    coreTop = float(params['core_flat_top'])
    # core height
    coreHt = float(params['core_height'])
    # outer dike slope
    dikeOutSlope = float(params['outer_dike_slope'])
    # inner dike slope
    dikeInSlope = float(params['inner_dike_slope'])
    # armor depth
    armorDepth = float(params['armor_depth'])

    # Calculate total height of structure
    totalHt = 5. - elev

    if totalHt <= 0.:
        # This implies that the dike height is very low and the elevation is very high.
        # Assume these areas don't really need a dike (over land). Negative numbers break
        # the routing algorithm, so set everything to 0.
        dikeVolume = 0.0
        coreVolume = 0.0
        toeVolume = 0.0
        armorVolume = 0.0
        foundVolume = 0.0

    else:
        # parallelogram toe
        toeBase = 5.
        toeVolume = toeHeight * toeBase

        # trapezoidal berm
        # determine berm height based on total structure height
        dikeHt = totalHt / 3.
        if dikeHt < 1.5:
            dikeHt = 0.

        # volume of trapezoid
        dikeVolume = (dikeOutSlope + dikeInSlope) / 2. * dikeHt ** 2. + dikeTop * dikeHt

        # caisson core
        # determine caisson height based on total structure height
        caissonHt = totalHt - dikeHt

        # determine caisson core height, based on a cap thickness of 4.5 meters
        if caissonHt <= 4.5:
            coreHt = 0.
        else:
            coreHt = caissonHt - 4.5

        # calculate caisson core volume
        coreVolume = coreTop * coreHt * length

        # foundation just a rectangle under the base
        foundBase = (dikeOutSlope + dikeInSlope) * dikeHt + dikeTop
        foundVolume = foundBase * foundHt * length

        # armoring - find surface area of dike, then add a layer of armoring
        surfaceArea = (((dikeOutSlope * dikeHt) ** 2.0 + dikeHt ** 2.0) ** 0.5 + \
                       ((dikeInSlope * dikeHt) ** 2.0 + dikeHt ** 2.0) ** 0.5 + \
                       dikeTop - coreTop) * length
        dikeArmorVolume = surfaceArea * armorDepth
        concreteCapVolume = (caissonHt - coreHt) * coreTop * length
        # armor is sume of dike armor and concrete cap
        armorVolume = dikeArmorVolume + concreteCapVolume
        print ""
    # for purposes of the algorithm, the dike volume can proxy for the cost
    return {   'toeVol': toeVolume,
                'coreVol' : coreVolume,
                'dikeVol' : dikeVolume,
                'foundVol' : foundVolume,
                'armorVol' : armorVolume,
                'cost' : dikeVolume + coreVolume + toeVolume + foundVolume + armorVolume
            }


# Nathan Chase's SUPERSLR Design
# Implemented by Keith Mosher
def multiDikeSingleBermCombo(length, elev, params):
    # Set parameters
    # sea level rise height
    slr = float(params['sea_level_rise'])
    # freeboard height
    freeboard = float(params['freeboard'])
    # design wave height
    wave = float(params['design_wave_height'])
    # storm surge height
    surge = float(params['storm_surge'])
    # mean high-high tide height
    highTide = float(params['mean_high_high_tide'])
    # mean low-low tide height
    lowTide = float(params['mean_low_low_tide'])
    # dike flat top width
    dikeTop = float(params['dike_flat_top'])
    # foundation height
    foundHt = float(params['foundation_height'])
    # toe height
    toeHt = float(params['toe_height'])
    # outer toe slope
    toeOutSlope = float(params['outer_toe_slope'])
    # inner toe slope
    toeInSlope = float(params['inner_toe_slope'])
    # outer core slope
    coreOutSlope = float(params['outer_core_slope'])
    # inner core slope
    coreInSlope = float(params['inner_core_slope'])
    # core flat top
    coreTop = float(params['core_flat_top'])
    # core height
    coreHt = float(params['core_height'])
    # outer dike slope
    dikeOutSlope = float(params['outer_dike_slope'])
    # inner dike slope
    dikeInSlope = float(params['inner_dike_slope'])
    # armor depth
    armorDepth = float(params['armor_depth'])



   # triangular toe
    toeBase = toeOutSlope * toeHt + toeInSlope * toeHt
    toeVolume = 0.5 * toeBase * toeHt * length

    # trapezoidal core
    coreBase = coreInSlope * coreHt + coreOutSlope * coreHt + coreTop
    coreVolume = 0.5 * (coreBase + coreTop) * coreHt * length

    # trapezoidal shape
    dikeHt = highTide + surge + wave + freeboard + slr - elev
    dikeBase = dikeOutSlope * dikeHt + dikeInSlope * dikeHt + dikeTop
    # volume of trapezoid, but subtract out toe and core volumes
    dikeVolume = 0.5 * (dikeBase + dikeTop) * dikeHt * length - toeVolume - coreVolume

    # foundation just a rectangle under the base
    foundBase = toeBase + dikeBase
    foundVolume = foundBase * foundHt * length

    # armoring - find surface area of dike, then add a layer of armoring
    outerSurfaceArea = ((dikeOutSlope * dikeHt) ** 2.0 + dikeHt ** 2.0) ** 0.5 * length
    innerSurfaceArea = ((dikeInSlope * dikeHt) ** 2.0 + dikeHt ** 2.0) ** 0.5 * length
    surfaceArea = outerSurfaceArea + innerSurfaceArea
    armorVolume = surfaceArea * armorDepth

    if dikeVolume < 0.0:
        # This implies that the dike height is very low and the elevation is very high.
        # Assume these areas don't really need a dike (over land). Negative numbers break
        # the routing algorithm, so set everything to 0 (changing to .1 to encourage shorter paths -km).
        dikeVolume = 0.10
        coreVolume = 0.10
        toeVolume = 0.10
        armorVolume = 0.10
        foundVolume = 0.10


    max_depth = float(params['min_elevation'])
    #print "KMB2 length: %s elev: %s max_depth: %s" % (length, elev, max_depth)

    if elev > 0 :
        leeside_armor_berm_depth = 1
        #print "berm"
    elif elev <=0 and elev > -10 :
        leeside_armor_berm_depth = 1
        #print "rubble mound breakwater"
    elif elev <= -10 and elev >= max_depth :
        #print "deep breakwater"

        # core part 1
        core_depth = 2. #D25
        if elev < -25.:
            core_depth = 2. + (((-elev) - 25.) / 3.) #D25 #=IF(D14<25,2,2+(D14-25)/3)

        # leeside_armor_berm
        leeside_armor_berm_depth = 2. #D95
        leeside_armor_berm_width_toe = 3. #D96
        leeside_armor_berm_slope_1v = 2. #D97
        leeside_armor_berm_width_top = 3. #D98
        leeside_armor_berm_width_sloped = (core_depth - (leeside_armor_berm_depth * 2.)) * leeside_armor_berm_slope_1v   #D99 #=(D25-D95*2)*D97
        leeside_armor_berm_width_total = leeside_armor_berm_width_toe + leeside_armor_berm_width_top + leeside_armor_berm_width_sloped #D100 #=D99+D96+D98
        #D101 length
        leeside_armor_berm_volume = leeside_armor_berm_depth * leeside_armor_berm_width_total * length #D102 #=D95*D100*D101

        # leeside_mass
        leeside_mass_number_of_units = 1. #D88
        leeside_mass_depth = 2. #D89
        leeside_mass_width = 2. #D90
        #D91 length
        leeside_mass_volume = leeside_mass_number_of_units * leeside_mass_depth * leeside_mass_width * length #D92 #=D95*D100*D101

        # caisson_cap
        caisson_cap_depth = 2. #D82
        caisson_cap_width = 11. #D83
        #D84 length
        caisson_cap_volume = caisson_cap_depth * caisson_cap_width * length #D85 #=D82*D83*D84

        # rectangular_caissons
        rectangular_caissons_number_of_units = 2. #D72
        rectangular_caissons_depth = (25. - 2.) + ((2. / 3.) * ((-elev) - 25.)) #(height) #D73 #=25-2+2/3*(D14-25) #=IF(D14<25,25-D25,25-2+2/3*(D14-25))
        if elev > -25:
            rectangular_caissons_depth = 25. - core_depth #(height) #D73 #=25-D25 #=IF(D14<25,25-D25,25-2+2/3*(D14-25))
        rectangular_caissons_width = 5. #D74
        #D75 length
        rectangular_caissons_wall_thickness = 0.5 #D76
        rectangular_caissons_base_slab_thickness = 1.5 #D77
        rectangular_caissons_volume_concrete = ((rectangular_caissons_depth * rectangular_caissons_width) - ((rectangular_caissons_width - 2. * rectangular_caissons_wall_thickness) * (rectangular_caissons_depth - rectangular_caissons_base_slab_thickness))) * length * rectangular_caissons_number_of_units #D78 #=((D73*D74)-((D74-2*D76)*(D73-D77)))*D75*D72
        rectangular_caissons_volume_sand = ((rectangular_caissons_width - 2. * rectangular_caissons_wall_thickness) * (rectangular_caissons_depth - rectangular_caissons_base_slab_thickness)) * length * rectangular_caissons_number_of_units #D79 #=((D74-2*D76)*(D73-D77))*D75*D72

        # sloped_caissons
        sloped_caissons_number_of_units = 2. #D61
        sloped_caissons_depth = (25. - 2.) + (2. / 3.) * ((-elev) - 25.) #(height) #D62 #=25-2+2/3*(D14-25) #=IF(D14<25,25-D25,25-2+2/3*(D14-25))
        if elev > -25:
            sloped_caissons_depth = 25. - core_depth #(height) #D62 #=25-D25
        sloped_caissons_slope_1h = 6. #D64
        sloped_caissons_width = sloped_caissons_depth / sloped_caissons_slope_1h #D63 #=D62/D64
        #D65 length
        sloped_caissons_wall_thickness = 0.5 #D66
        sloped_caissons_base_slab_thickness = 1.5 #D67
        sloped_caissons_volume_concrete = ((sloped_caissons_depth * sloped_caissons_width / 2.) -  (((sloped_caissons_width - 2. * sloped_caissons_wall_thickness) * (sloped_caissons_depth - sloped_caissons_base_slab_thickness)) / 2.)) * length * sloped_caissons_number_of_units #D68 #=((D62*D63/2)-((D63-2*D66)*(D62-D67))/2)*D65*D61
        sloped_caissons_volume_sand = ((sloped_caissons_width - (2. * sloped_caissons_wall_thickness)) * (sloped_caissons_depth - sloped_caissons_base_slab_thickness) / 2.) * length * sloped_caissons_number_of_units#D69 #=(D63-2*D66)*(D62-D67)/2*D65*D61

        # primary_mass
        primary_mass_number_of_units = 2. #D54
        primary_mass_depth = 2. #(height) #D55
        primary_mass_width = 2. #D56
        #D57 length
        primary_mass_volume = primary_mass_number_of_units * primary_mass_depth * primary_mass_width * length #D58 #=D54*D55*D56*D57

        # leveling_course
        leveling_course_depth = 0.5 #D48
        leveling_course_width = primary_mass_number_of_units * primary_mass_width + caisson_cap_width + leeside_mass_number_of_units * leeside_mass_width #D49 #=D54*D56+D83+D88*D90
        #D50 length
        leveling_course_volume = leveling_course_depth * leveling_course_width * length #D51 #=D48*D49*D50

        # primary_armor_berm
        primary_armor_berm_depth = 2. #D38
        primary_armor_berm_width_toe = 3. #D39
        primary_armor_berm_slope_1v = 2. #D40
        primary_armor_berm_width_top = 3. #D41
        primary_armor_berm_width_sloped =  (core_depth - (primary_armor_berm_depth * 2.)) * primary_armor_berm_slope_1v #D42  #=(D25-D38*2)*D40
        primary_armor_berm_width_total = primary_armor_berm_width_sloped + primary_armor_berm_width_toe + primary_armor_berm_width_top #D43  #=D42+D39+D41
        #D44 length
        primary_armor_berm_volume = primary_armor_berm_depth * primary_armor_berm_width_total * length #D45

        # scour_blanket_toe_berm
        scour_blanket_toe_berm_depth = 1. #D31
        scour_blanket_toe_berm_width_exposed = 5. #D32
        scour_blanket_toe_berm_width_total = scour_blanket_toe_berm_width_exposed + primary_armor_berm_width_total #D33  #=D32+D43
        #D34 length
        scour_blanket_toe_berm_volume = scour_blanket_toe_berm_depth * scour_blanket_toe_berm_width_total * length #D35

        # core part 2
        core_width =  primary_armor_berm_width_sloped + primary_armor_berm_width_top + (primary_mass_number_of_units * primary_mass_width) + (sloped_caissons_width * sloped_caissons_number_of_units) + (rectangular_caissons_number_of_units * rectangular_caissons_width) + (leeside_mass_number_of_units * leeside_mass_depth) + leeside_armor_berm_width_top + leeside_armor_berm_width_sloped #D26  #D42+D41+D54*D56+D63*D61+D72*D74+D88*D89+D98+D99
        #D27 length
        core_volume = core_depth * core_width * length  #D28 #=D25*D26*D27

        # dredge_and_replace
        dredge_and_replace_depth = 1. #D19
        dredge_and_replace_width = leeside_armor_berm_width_toe + core_width + scour_blanket_toe_berm_width_exposed + primary_armor_berm_width_toe #D20 #=D26+D32+D39+D96
        #D21 length
        dredge_and_replace_volume = dredge_and_replace_depth * dredge_and_replace_width * length #D22 #=D19*D20*D21

# D14   elev





    else :
        print "error, dike model only operates to max depth %s" % (max_depth)



    # for purposes of the algorithm, the dike volume can proxy for the cost
    return {   'toeVol': toeVolume,
               'elev': elev,
               'length': length,
               'coreVol' : coreVolume,
               'dikeVol' : dikeVolume,
               'foundVol' : foundVolume,
               'armorVol' : armorVolume,
               'cost' : dikeVolume + coreVolume + toeVolume + foundVolume + armorVolume
            }


# Nathan Chase's SUPERSLR Design
# Implemented by Keith Mosher
def multiDikeSingleBermComboTest(length, elev, max_depth):

    if elev > 0 :
        leeside_armor_berm_depth = 1
        #print "berm"
    elif elev <=0 and elev > -10 :
        leeside_armor_berm_depth = 1
        #print "rubble mound breakwater"
    elif elev <= -10 and elev >= max_depth :
        #print "deep breakwater"




        # core part 1
        core_depth = 2. #D25
        if elev < -25.:
            core_depth = 2. + (((-elev) - 25.) / 3.) #D25 #=IF(D14<25,2,2+(D14-25)/3)

        # leeside_armor_berm
        leeside_armor_berm_depth = 2. #D95
        leeside_armor_berm_width_toe = 3. #D96
        leeside_armor_berm_slope_1v = 2. #D97
        leeside_armor_berm_width_top = 3. #D98
        leeside_armor_berm_width_sloped = (core_depth - (leeside_armor_berm_depth * 2.)) * leeside_armor_berm_slope_1v   #D99 #=(D25-D95*2)*D97
        leeside_armor_berm_width_total = leeside_armor_berm_width_toe + leeside_armor_berm_width_top + leeside_armor_berm_width_sloped #D100 #=D99+D96+D98
        #D101 length
        leeside_armor_berm_volume = leeside_armor_berm_depth * leeside_armor_berm_width_total * length #D102 #=D95*D100*D101

        # leeside_mass
        leeside_mass_number_of_units = 1. #D88
        leeside_mass_depth = 2. #D89
        leeside_mass_width = 2. #D90
        #D91 length
        leeside_mass_volume = leeside_mass_number_of_units * leeside_mass_depth * leeside_mass_width * length #D92 #=D95*D100*D101

        # caisson_cap
        caisson_cap_depth = 2. #D82
        caisson_cap_width = 11. #D83
        #D84 length
        caisson_cap_volume = caisson_cap_depth * caisson_cap_width * length #D85 #=D82*D83*D84

        # rectangular_caissons
        rectangular_caissons_number_of_units = 2. #D72
        rectangular_caissons_depth = (25. - 2.) + ((2. / 3.) * ((-elev) - 25.)) #(height) #D73 #=25-2+2/3*(D14-25) #=IF(D14<25,25-D25,25-2+2/3*(D14-25))
        if elev > -25:
            rectangular_caissons_depth = 25. - core_depth #(height) #D73 #=25-D25 #=IF(D14<25,25-D25,25-2+2/3*(D14-25))
        rectangular_caissons_width = 5. #D74
        #D75 length
        rectangular_caissons_wall_thickness = 0.5 #D76
        rectangular_caissons_base_slab_thickness = 1.5 #D77
        rectangular_caissons_volume_concrete = ((rectangular_caissons_depth * rectangular_caissons_width) - ((rectangular_caissons_width - 2. * rectangular_caissons_wall_thickness) * (rectangular_caissons_depth - rectangular_caissons_base_slab_thickness))) * length * rectangular_caissons_number_of_units #D78 #=((D73*D74)-((D74-2*D76)*(D73-D77)))*D75*D72
        rectangular_caissons_volume_sand = ((rectangular_caissons_width - 2. * rectangular_caissons_wall_thickness) * (rectangular_caissons_depth - rectangular_caissons_base_slab_thickness)) * length * rectangular_caissons_number_of_units #D79 #=((D74-2*D76)*(D73-D77))*D75*D72

        # sloped_caissons
        sloped_caissons_number_of_units = 2. #D61
        sloped_caissons_depth = (25. - 2.) + (2. / 3.) * ((-elev) - 25.) #(height) #D62 #=25-2+2/3*(D14-25) #=IF(D14<25,25-D25,25-2+2/3*(D14-25))
        if elev > -25:
            sloped_caissons_depth = 25. - core_depth #(height) #D62 #=25-D25
        sloped_caissons_slope_1h = 6. #D64
        sloped_caissons_width = sloped_caissons_depth / sloped_caissons_slope_1h #D63 #=D62/D64
        #D65 length
        sloped_caissons_wall_thickness = 0.5 #D66
        sloped_caissons_base_slab_thickness = 1.5 #D67
        sloped_caissons_volume_concrete = ((sloped_caissons_depth * sloped_caissons_width / 2.) -  (((sloped_caissons_width - 2. * sloped_caissons_wall_thickness) * (sloped_caissons_depth - sloped_caissons_base_slab_thickness)) / 2.)) * length * sloped_caissons_number_of_units #D68 #=((D62*D63/2)-((D63-2*D66)*(D62-D67))/2)*D65*D61
        sloped_caissons_volume_sand = ((sloped_caissons_width - (2. * sloped_caissons_wall_thickness)) * (sloped_caissons_depth - sloped_caissons_base_slab_thickness) / 2.) * length * sloped_caissons_number_of_units#D69 #=(D63-2*D66)*(D62-D67)/2*D65*D61

        # primary_mass
        primary_mass_number_of_units = 2. #D54
        primary_mass_depth = 2. #(height) #D55
        primary_mass_width = 2. #D56
        #D57 length
        primary_mass_volume = primary_mass_number_of_units * primary_mass_depth * primary_mass_width * length #D58 #=D54*D55*D56*D57

        # leveling_course
        leveling_course_depth = 0.5 #D48
        leveling_course_width = primary_mass_number_of_units * primary_mass_width + caisson_cap_width + leeside_mass_number_of_units * leeside_mass_width #D49 #=D54*D56+D83+D88*D90
        #D50 length
        leveling_course_volume = leveling_course_depth * leveling_course_width * length #D51 #=D48*D49*D50

        # primary_armor_berm
        primary_armor_berm_depth = 2. #D38
        primary_armor_berm_width_toe = 3. #D39
        primary_armor_berm_slope_1v = 2. #D40
        primary_armor_berm_width_top = 3. #D41
        primary_armor_berm_width_sloped =  (core_depth - (primary_armor_berm_depth * 2.)) * primary_armor_berm_slope_1v #D42  #=(D25-D38*2)*D40
        primary_armor_berm_width_total = primary_armor_berm_width_sloped + primary_armor_berm_width_toe + primary_armor_berm_width_top #D43  #=D42+D39+D41
        #D44 length
        primary_armor_berm_volume = primary_armor_berm_depth * primary_armor_berm_width_total * length #D45

        # scour_blanket_toe_berm
        scour_blanket_toe_berm_depth = 1. #D31
        scour_blanket_toe_berm_width_exposed = 5. #D32
        scour_blanket_toe_berm_width_total = scour_blanket_toe_berm_width_exposed + primary_armor_berm_width_total #D33  #=D32+D43
        #D34 length
        scour_blanket_toe_berm_volume = scour_blanket_toe_berm_depth * scour_blanket_toe_berm_width_total * length #D35

        # core part 2
        core_width =  primary_armor_berm_width_sloped + primary_armor_berm_width_top + (primary_mass_number_of_units * primary_mass_width) + (sloped_caissons_width * sloped_caissons_number_of_units) + (rectangular_caissons_number_of_units * rectangular_caissons_width) + (leeside_mass_number_of_units * leeside_mass_depth) + leeside_armor_berm_width_top + leeside_armor_berm_width_sloped #D26  #D42+D41+D54*D56+D63*D61+D72*D74+D88*D89+D98+D99
        #D27 length
        core_volume = core_depth * core_width * length  #D28 #=D25*D26*D27

        # dredge_and_replace
        dredge_and_replace_depth = 1. #D19
        dredge_and_replace_width = leeside_armor_berm_width_toe + core_width + scour_blanket_toe_berm_width_exposed + primary_armor_berm_width_toe #D20 #=D26+D32+D39+D96
        #D21 length
        dredge_and_replace_volume = dredge_and_replace_depth * dredge_and_replace_width * length #D22 #=D19*D20*D21

# D14   elev





# D14
        print elev
        print dredge_and_replace_depth
        print dredge_and_replace_width
        print length
        print dredge_and_replace_volume #D22 #=D19*D20*D21
        print
        print

        print core_depth #D25
        print core_width  #D26  #D42+D41+D54*D56+D63*D61+D72*D74+D88*D89+D98+D99
        #D27 length
        print length
        print core_volume  #D28 #=D25*D26*D27

        print
        print
        # scour_blanket_toe_berm
        print scour_blanket_toe_berm_depth #D31
        print scour_blanket_toe_berm_width_exposed #D32
        print scour_blanket_toe_berm_width_total #D33  #=D32+D43
        #D34 length
        print length
        print scour_blanket_toe_berm_volume  #D35

        print
        print
        # primary_armor_berm
        print primary_armor_berm_depth #D38
        print primary_armor_berm_width_toe  #D39
        print primary_armor_berm_slope_1v #D40
        print primary_armor_berm_width_top  #D41
        print primary_armor_berm_width_sloped  #D42  #=(D25-D38*2)*D40
        print primary_armor_berm_width_total  #D43  #=D42+D39+D41
        #D44 length
        print length
        print primary_armor_berm_volume  #D45

        print
        print
        # leveling_course
        print leveling_course_depth  #D48
        print leveling_course_width #D49 #=D54*D56+D83+D88*D90
        #D50 length
        print length
        print leveling_course_volume  #D51 #=D48*D49*D50
        print
        print
        # primary_mass
        print primary_mass_number_of_units #D54
        print primary_mass_depth #(height) #D55
        print primary_mass_width #D56
        #D57 length
        print length
        print primary_mass_volume  #D58 #=D54*D55*D56*D57

        print
        print
        # sloped_caissons
        print sloped_caissons_number_of_units  #D61
        print sloped_caissons_depth  #(height) #D62 #=25-2+2/3*(D14-25) #=IF(D14<25,25-D25,25-2+2/3*(D14-25))
        print sloped_caissons_width #D63 #=D62/D64
        print sloped_caissons_slope_1h  #D64
        #D65 length
        print length
        print sloped_caissons_wall_thickness #D66
        print sloped_caissons_base_slab_thickness  #D67
        print sloped_caissons_volume_concrete  #D68 #=((D62*D63/2)-((D63-2*D66)*(D62-D67))/2)*D65*D61
        print sloped_caissons_volume_sand #D69 #=(D63-2*D66)*(D62-D67)/2*D65*D61

        print
        print
        # rectangular_caissons
        print rectangular_caissons_number_of_units  #D72
        print rectangular_caissons_depth #(height) #D73 #=25-2+2/3*(D14-25) #=IF(D14<25,25-D25,25-2+2/3*(D14-25))
        print rectangular_caissons_width #D74
        #D75 length
        print length
        print rectangular_caissons_wall_thickness  #D76
        print rectangular_caissons_base_slab_thickness #D77
        print rectangular_caissons_volume_concrete #D78 #=((D73*D74)-((D74-2*D76)*(D73-D77)))*D75*D72
        print rectangular_caissons_volume_sand  #D79 #=((D74-2*D76)*(D73-D77))*D75*D72

        print
        print
        # caisson_cap
        print caisson_cap_depth  #D82
        print caisson_cap_width  #D83
        #D84 length
        print length
        print caisson_cap_volume  #D85 #=D82*D83*D84

        print
        print
        # leeside_mass
        print leeside_mass_number_of_units #D88
        print leeside_mass_depth #D89
        print leeside_mass_width #D90
        #D91 length
        print length
        print leeside_mass_volume #D92 #=D95*D100*D101


        print
        print
        # leeside_armor_berm
        print leeside_armor_berm_depth #D95
        print leeside_armor_berm_width_toe  #D96
        print leeside_armor_berm_slope_1v #D97
        print leeside_armor_berm_width_top #D98
        print leeside_armor_berm_width_sloped #D99 #=(D25-D95*2)*D97
        print leeside_armor_berm_width_total #D100 #=D99+D96+D98
        #D101 length
        print length
        print leeside_armor_berm_volume #D102 #=D95*D100*D101







        print
        print
        print
        print
        print elev
        print dredge_and_replace_width
        print dredge_and_replace_volume #D22 #=D19*D20*D21
        print core_depth #D25
        print core_width  #D26  #D42+D41+D54*D56+D63*D61+D72*D74+D88*D89+D98+D99=
        print core_volume  #D28 #=D25*D26*D27
        print scour_blanket_toe_berm_width_total #D33  #=D32+D43
        print
        print scour_blanket_toe_berm_volume  #D35
        print primary_armor_berm_width_total  #D43  #=D42+D39+D41
        print primary_armor_berm_volume  #D45
        print leveling_course_width #D49 #=D54*D56+D83+D88*D90
        print leveling_course_volume  #D51 #=D48*D49*D50
        print primary_mass_volume  #D58 #=D54*D55*D56*D57
        print sloped_caissons_depth  #(height) #D62 #=25-2+2/3*(D14-25) #=IF(D14<25,25-D25,25-2+2/3*(D14-25))
        print sloped_caissons_width #D63 #=D62/D64
        print sloped_caissons_volume_concrete  #D68 #=((D62*D63/2)-((D63-2*D66)*(D62-D67))/2)*D65*D61
        print
        print sloped_caissons_volume_sand #D69 #=(D63-2*D66)*(D62-D67)/2*D65*D61
        print rectangular_caissons_depth #(height) #D73 #=25-2+2/3*(D14-25) #=IF(D14<25,25-D25,25-2+2/3*(D14-25))
        print rectangular_caissons_volume_concrete #D78 #=((D73*D74)-((D74-2*D76)*(D73-D77)))*D75*D72
        print rectangular_caissons_volume_sand  #D79 #=((D74-2*D76)*(D73-D77))*D75*D72
        print caisson_cap_volume  #D85 #=D82*D83*D84=
        print leeside_mass_volume #D92 #=D95*D100*D101
        print leeside_armor_berm_width_sloped #D99 #=(D25-D95*2)*D97
        print leeside_armor_berm_width_total #D100 #=D99+D96+D98
        print leeside_armor_berm_volume #D102 #=D95*D100*D101



    else :
        print "error, dike model only operates to max depth %s" % (max_depth)




