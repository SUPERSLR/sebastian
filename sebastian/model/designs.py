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


# Nathan Chase's SUPERSLR Design 10/2013
# Implemented by Keith Mosher
def dikeOrBermSection(length, elev, params):
#    print "dikeOrBermSection"
    # This function has hard coded values for freeboard and maxdepth
    # They are defined in the spreadsheet with calculations for structure size and can't be modified
    #max_depth = float(params['min_elevation'])
    #freeboard = float(params['freeboard'])

    # Import math module for square roots
    import math

    # Set parameters
    # sea level rise height
    slr = float(params['sea_level_rise'])
    # design wave height
    wave = float(params['design_wave_height'])
    # storm surge height
    surge = float(params['storm_surge'])
    # mean high-high tide height
    highTide = float(params['mean_high_high_tide'])
    # mean low-low tide height
    lowTide = float(params['mean_low_low_tide'])

    sand = 0
    gravel = 0
    quarry_run_stone = 0
    large_riprap = 0
    small_riprap = 0
    concrete = 0
    structural_steel = 0
    cantilever_floodwall_length = 0
    cantilever_floodwall_height = 0
    rubble_breakwater_length = 0
    rubble_breakwater_height = 0
    caisson_breakwater_length = 0
    caisson_breakwater_height = 0


    #print "KMB2 length: %s elev: %s max_depth: %s" % (length, elev, max_depth)

    # havg will be different if it is for a floodwall or a breakwater
    # DWSEL = MHHW + SLR + (100-year Storm Surge * 1.1)
    # cantilever_floodwall
    # havg = avg (DWSEL + Freeboard - EG - 0.5m)
    # rubble_breakwater
    # havg = avg (DWSEL + Freeboard - EG)
    # caisson_breakwater
    # havg = avg (DWSEL + Freeboard - EG)

    # The best option is to use a floodwall, if it's too deep, a rubble breakwater, and if it's deeper than that then a caisson breakwater
    # In order to figure out what to use, calculate the floodwall and breakwater havg, and then find the minimum required structure

    #dwsel = highTide + slr + surge * 1.1
    # surge from DIVA and SurgeDat both contain MHHW, so don't explicitly include it
    dwsel = slr + surge * 1.1

    freeboard_floodwall = 0.9
    freeboard_breakwater = 0.6

    havg_floodwall = dwsel + freeboard_floodwall - elev - 0.5
    havg_breakwater = dwsel + freeboard_breakwater - elev

    cantilever_floodwall_min_havg = 0.0
    cantilever_floodwall_min_height = 2.0
    cantilever_floodwall_max_height = 10.0
    rubble_breakwater_min_havg = 0.0
    rubble_breakwater_min_height = 7.0
    rubble_breakwater_max_height = 15.0
    caisson_breakwater_min_havg = 15.0
    caisson_breakwater_min_height = 15.0
    caisson_breakwater_max_height = 60.0

    elev_no_structure_needed = dwsel + freeboard_floodwall
    no_structure_needed_optimization_cost = 0
    structure_type = 'none'

    if havg_floodwall <= cantilever_floodwall_max_height and elev < elev_no_structure_needed  :
        structure_type = 'floodwall'
        #print "berm"
        cantilever_floodwall_length = length #E10
        if havg_floodwall > cantilever_floodwall_min_height :
            cantilever_floodwall_height = havg_floodwall #E11
        else :
            cantilever_floodwall_height = cantilever_floodwall_min_height #E11
        rubble_breakwater_length = 0 #E12
        rubble_breakwater_height = 0 #E13
        caisson_breakwater_length = 0 #E14
        caisson_breakwater_height = 0 #E15
    elif havg_breakwater > rubble_breakwater_min_havg and havg_breakwater <= rubble_breakwater_max_height :
        structure_type = 'rubblemound'
        #print "rubble mound breakwater"
        cantilever_floodwall_length = 0 #E10
        cantilever_floodwall_height = 0 #E11
        rubble_breakwater_length = length #E12
        if havg_breakwater > rubble_breakwater_min_height :
            rubble_breakwater_height = havg_breakwater #E13
        else :
            rubble_breakwater_height = rubble_breakwater_min_height #E13
        caisson_breakwater_length = 0 #E14
        caisson_breakwater_height = 0 #E15
    #elif havg_breakwater >= caisson_breakwater_min_havg and havg_breakwater <= caisson_breakwater_max_height :
    elif havg_breakwater >= caisson_breakwater_min_havg and -elev <= caisson_breakwater_max_height :
        structure_type = 'caisson'
        #print "deep breakwater"
        cantilever_floodwall_length = 0 #E10
        cantilever_floodwall_height = 0 #E11
        rubble_breakwater_length = 0 #E12
        rubble_breakwater_height = 0 #E13
        caisson_breakwater_length = length #E14
        caisson_breakwater_height = havg_breakwater #E15
    # It was decided that the caisson breakwater can be as tall as it needs
    # to be, but can only be in water up to -60 m.  This is handled upstream,
    # as deeper than -60 sections should have been removed before simulation.
    #elif havg_breakwater > caisson_breakwater_max_height :
    elif -elev > caisson_breakwater_max_height :
        print "error, water too deep"
        #TODO: how to return deep error?
        cantilever_floodwall_length = 99999999 #E10
        cantilever_floodwall_height = 99999999 #E11
        rubble_breakwater_length = 99999999 #E12
        rubble_breakwater_height = 99999999 #E13
        caisson_breakwater_length = 99999999 #E14
        caisson_breakwater_height = 99999999 #E15
    else :
        # Existing Grade (EG) is greater than Design Water Surface ELevation (DWSEL), no structure needed
        #print "safe elevation, no structure needed"
        # Add a small value to volume per unit length to avoid long
        # paths which all have equivalent 0 cost
        no_structure_needed_optimization_cost = length / 9999.0
        cantilever_floodwall_length = 0 #E10
        cantilever_floodwall_height = 0 #E11
        rubble_breakwater_length = 0 #E12
        rubble_breakwater_height = 0 #E13
        caisson_breakwater_length = 0 #E14
        caisson_breakwater_height = 0 #E15


    density_of_steel = 7850 # kg/m3 #$LUTs.D$3
    density_of_concrete = 2400 # kg/m3 #$LUTs.D$4

    # Caisson Breakwater Parameters
    #moved up to avoid ordering conflicts
    #E37 #core_quarry_run_stone_depth #if ('=IF(E15<25,2,2+(E15-25)/3)
    if ( caisson_breakwater_height < 25.0) :
        core_quarry_run_stone_depth  = 2.0
    else :
        core_quarry_run_stone_depth  = 2.0 + (( caisson_breakwater_height - 25.0) / 3.0)  #E37 #if ('=IF(E15<25,2,2+(E15-25)/3)
    scour_blanket_toe_berm_small_riprap_width_exposed = 5.0  #E44 #=5
    primary_armor_berm_large_riprap_width_toe = 3.0  #E51 #=3
    primary_armor_berm_large_riprap_depth = 2.0  #E50 #=2
    primary_armor_berm_large_riprap_slope = 2.0  #E52 #=2
    primary_armor_berm_large_riprap_width_top = 3.0  #E53 #=3
    leveling_course_gravel_depth = 0.5  #E60 #=0.5
    primary_mass_concrete_block_number_of_units = 2.0  #E66 #=2
    sloped_caissons_concrete_filled_with_sand_number_of_units = 2.0  #E73 #=2
    sloped_caissons_concrete_filled_with_sand_slope = 6.0  #E76 #=6
    #E78 #sloped_caissons_concrete_filled_with_sand_wall_thickness #if ('=IF(E$15<30,0.5,0.75)
    if ( caisson_breakwater_height < 30.0) :
        sloped_caissons_concrete_filled_with_sand_wall_thickness  = 0.5
    else :
        sloped_caissons_concrete_filled_with_sand_wall_thickness  = 0.75  #E78 #if ('=IF(E$15<30,0.5,0.75)
    rectangular_caissons_concrete_filled_with_sand_number_of_units = 2.0  #E84 #=2
    rectangular_caissons_concrete_filled_with_sand_base_width = 5.0  #E86 #=5
    caisson_cap_width = rectangular_caissons_concrete_filled_with_sand_number_of_units * rectangular_caissons_concrete_filled_with_sand_base_width + (2.0 * sloped_caissons_concrete_filled_with_sand_wall_thickness )  #E105 #='=E84*E86+2*E78
    leeside_mass_concrete_block_number_of_units = 1.0  #E116 #=1
    leeside_mass_concrete_block_height = max(1.5, ( caisson_breakwater_height / 20.0))  #E117 #='=MAX(1.5,E$15/20)
    leeside_mass_concrete_block_width = max(1.5, ( caisson_breakwater_height / 20.0))  #E118 #='=MAX(1.5,E$15/20)
    leeside_armor_berm_large_riprap_width_toe = 3.0  #E124 #=3
    leeside_armor_berm_large_riprap_depth = 2.0  #E123 #=2
    leeside_armor_berm_large_riprap_slope_1v = 2.0  #E125 #=2
    leeside_armor_berm_large_riprap_width_top = 3.0  #E126 #=3
    leeside_armor_berm_large_riprap_width_sloped = ( core_quarry_run_stone_depth - (2.0 * leeside_armor_berm_large_riprap_depth )) * leeside_armor_berm_large_riprap_slope_1v  #E127 #='=(E37-E123*2)*E125

    primary_armor_berm_large_riprap_width_sloped = ( core_quarry_run_stone_depth - ( primary_armor_berm_large_riprap_depth * 2.0 )) * primary_armor_berm_large_riprap_slope  #E54 #='=(E37-E50*2)*E52
    primary_mass_concrete_block_width = max(1.5, ( caisson_breakwater_height / 20.0))  #E68 #='=MAX(1.5,E$15/20)
    primary_armor_berm_large_riprap_width_total = primary_armor_berm_large_riprap_width_sloped + primary_armor_berm_large_riprap_width_toe + primary_armor_berm_large_riprap_width_top  #E55 #='=E54+E51+E53

    #E74 #if ('=IF(E$15<25,E$15-E$37-E$60,25-2+2/3*(E$15-25-E$60))
    if ( caisson_breakwater_height < 25.0) :
        sloped_caissons_concrete_filled_with_sand_height = caisson_breakwater_height - core_quarry_run_stone_depth - leveling_course_gravel_depth
    else :
        sloped_caissons_concrete_filled_with_sand_height  = 25.0 - 2.0 + (2.0 / 3.0 * ( caisson_breakwater_height - 25.0 - leveling_course_gravel_depth ))
    sloped_caissons_concrete_filled_with_sand_base_width = sloped_caissons_concrete_filled_with_sand_height / sloped_caissons_concrete_filled_with_sand_slope  #E75 #='=E74/E76
    core_quarry_run_stone_width = primary_armor_berm_large_riprap_width_sloped + primary_armor_berm_large_riprap_width_top + ( primary_mass_concrete_block_number_of_units * primary_mass_concrete_block_width ) + ( sloped_caissons_concrete_filled_with_sand_base_width * sloped_caissons_concrete_filled_with_sand_number_of_units ) + ( rectangular_caissons_concrete_filled_with_sand_number_of_units * rectangular_caissons_concrete_filled_with_sand_base_width ) + ( leeside_mass_concrete_block_number_of_units * leeside_mass_concrete_block_height ) + leeside_armor_berm_large_riprap_width_top + leeside_armor_berm_large_riprap_width_sloped  #E38 #='=E54+E53+E66*E68+E75*E73+E84*E86+E116*E117+E126+E127

    freeboard = 0.6  #E28 #=0.6

    # dredge_and_replace_with_quarry_run_stone
    dredge_and_replace_with_quarry_run_stone_depth = 1.0  #E31 #=1

    dredge_and_replace_with_quarry_run_stone_width = core_quarry_run_stone_width + scour_blanket_toe_berm_small_riprap_width_exposed + primary_armor_berm_large_riprap_width_toe + leeside_armor_berm_large_riprap_width_toe  #E32 #='=E38+E44+E51+E124
    dredge_and_replace_with_quarry_run_stone_length = caisson_breakwater_length  #E33 #='=E$14
    dredge_and_replace_with_quarry_run_stone_volume_caisson = dredge_and_replace_with_quarry_run_stone_depth * dredge_and_replace_with_quarry_run_stone_width * dredge_and_replace_with_quarry_run_stone_length  #E34 #='=E31*E32*E33

    # core_quarry_run_stone
    core_quarry_run_stone_length = caisson_breakwater_length  #E39 #='=E$14
    core_quarry_run_stone_volume_caisson = core_quarry_run_stone_depth * core_quarry_run_stone_width * core_quarry_run_stone_length  #E40 #='=E37*E38*E39

    # scour_blanket_toe_berm_small_riprap
    scour_blanket_toe_berm_small_riprap_depth = 1.0  #E43 #=1
    scour_blanket_toe_berm_small_riprap_width_total = scour_blanket_toe_berm_small_riprap_width_exposed + primary_armor_berm_large_riprap_width_total  #E45 #='=E44+E55
    scour_blanket_toe_berm_small_riprap_length = caisson_breakwater_length  #E46 #='=E$14
    scour_blanket_toe_berm_small_riprap_volume = scour_blanket_toe_berm_small_riprap_depth * scour_blanket_toe_berm_small_riprap_width_total * scour_blanket_toe_berm_small_riprap_length  #E47 #='=E43*E45*E46

    # primary_armor_berm_large_riprap
    primary_armor_berm_large_riprap_length = caisson_breakwater_length  #E56 #='=E$14
    primary_armor_berm_large_riprap_volume = primary_armor_berm_large_riprap_depth * primary_armor_berm_large_riprap_width_total * primary_armor_berm_large_riprap_length  #E57 #='=E50*E55*E56

    # leveling_course_gravel
    leveling_course_gravel_width_total = ( primary_mass_concrete_block_number_of_units * primary_mass_concrete_block_width ) + caisson_cap_width + ( leeside_mass_concrete_block_number_of_units * leeside_mass_concrete_block_width )  #E61 #='=E66*E68+E105+E116*E118
    leveling_course_gravel_length = caisson_breakwater_length  #E62 #='=E$14
    leveling_course_gravel_volume = leveling_course_gravel_depth * leveling_course_gravel_width_total * leveling_course_gravel_length  #E63 #='=E60*E61*E62

    # dredge_and_replace_with_quarry_run_stone
    primary_mass_concrete_block_height = max(1.5, ( caisson_breakwater_height / 20.0))  #E67 #='=MAX(1.5,E$15/20)
    primary_mass_concrete_block_length = caisson_breakwater_length  #E69 #='=E$14
    primary_mass_concrete_block_volume = primary_mass_concrete_block_number_of_units * primary_mass_concrete_block_height * primary_mass_concrete_block_width * primary_mass_concrete_block_length  #E70 #='=E66*E67*E68*E69

    # sloped_caissons_concrete_filled_with_sand
    sloped_caissons_concrete_filled_with_sand_length = caisson_breakwater_length  #E77 #='=E$14
    sloped_caissons_concrete_filled_with_sand_base_slab_thickness = max(1.5, ( caisson_breakwater_height / 20.0))  #E79 #='=MAX(1.5,E$15/20)
    sloped_caissons_concrete_filled_with_sand_volume_concrete = (( sloped_caissons_concrete_filled_with_sand_height * ( sloped_caissons_concrete_filled_with_sand_base_width / 2.0)) - (( sloped_caissons_concrete_filled_with_sand_base_width - (2.0 * sloped_caissons_concrete_filled_with_sand_wall_thickness )) * ( sloped_caissons_concrete_filled_with_sand_height - sloped_caissons_concrete_filled_with_sand_base_slab_thickness - sloped_caissons_concrete_filled_with_sand_wall_thickness )) / 2.0 ) * sloped_caissons_concrete_filled_with_sand_length * sloped_caissons_concrete_filled_with_sand_number_of_units  #E80 #='=((E74*E75/2)-((E75-2*E78)*(E74-E79-E78))/2)*E77*E73

    sloped_caissons_concrete_filled_with_sand_volume_sand = ( sloped_caissons_concrete_filled_with_sand_base_width - (2.0 * sloped_caissons_concrete_filled_with_sand_wall_thickness )) * (( sloped_caissons_concrete_filled_with_sand_height - sloped_caissons_concrete_filled_with_sand_base_slab_thickness - sloped_caissons_concrete_filled_with_sand_wall_thickness ) / 2.0) * sloped_caissons_concrete_filled_with_sand_length * sloped_caissons_concrete_filled_with_sand_number_of_units  #E81 #='=(E75-2*E78)*(E74-E79-E78)/2*E77*E73

    # rectangular_caissons_concrete_filled_with_sand
    rectangular_caissons_concrete_filled_with_sand_height = sloped_caissons_concrete_filled_with_sand_height  #E85 #='=E74
    rectangular_caissons_concrete_filled_with_sand_length = caisson_breakwater_length  #E87 #='=E$14
    #rectangular_caissons_concrete_filled_with_sand_wall_thickness  #E88 #if ('=IF(E$15<30,0.5,0.75)
    if ( caisson_breakwater_height < 30.0) :
        rectangular_caissons_concrete_filled_with_sand_wall_thickness  = 0.5
    else :
        rectangular_caissons_concrete_filled_with_sand_wall_thickness  = 0.75
    rectangular_caissons_concrete_filled_with_sand_base_slab_thickness = max(1.5, ( caisson_breakwater_height / 20.0))  #E89 #='=MAX(1.5,E$15/20)
    rectangular_caissons_concrete_filled_with_sand_volume_concrete = (( rectangular_caissons_concrete_filled_with_sand_height * rectangular_caissons_concrete_filled_with_sand_base_width ) - (( rectangular_caissons_concrete_filled_with_sand_base_width - (2.0 * rectangular_caissons_concrete_filled_with_sand_wall_thickness )) * ( rectangular_caissons_concrete_filled_with_sand_height - rectangular_caissons_concrete_filled_with_sand_base_slab_thickness - rectangular_caissons_concrete_filled_with_sand_wall_thickness ))) *  rectangular_caissons_concrete_filled_with_sand_length * rectangular_caissons_concrete_filled_with_sand_number_of_units  #E90 #='=((E85*E86)-((E86-2*E88)*(E85-E89-E88)))*E87*E84

    rectangular_caissons_concrete_filled_with_sand_volume_sand = (( rectangular_caissons_concrete_filled_with_sand_base_width - (2.0 * rectangular_caissons_concrete_filled_with_sand_wall_thickness )) * ( rectangular_caissons_concrete_filled_with_sand_height - rectangular_caissons_concrete_filled_with_sand_base_slab_thickness - rectangular_caissons_concrete_filled_with_sand_wall_thickness )) * rectangular_caissons_concrete_filled_with_sand_length * rectangular_caissons_concrete_filled_with_sand_number_of_units  #E91 #='=((E86-2*E88)*(E85-E89-E88))*E87*E84

    # intermediate_caisson_walls
    intermediate_caisson_walls_spacing_interval = 6.0  #E95 #=6
    intermediate_caisson_walls_number_of_units = caisson_breakwater_length / intermediate_caisson_walls_spacing_interval  #E96 #='=E$14/E95
    intermediate_caisson_walls_height = rectangular_caissons_concrete_filled_with_sand_height  #E97 #='=E85
    intermediate_caisson_walls_base_width = rectangular_caissons_concrete_filled_with_sand_number_of_units * rectangular_caissons_concrete_filled_with_sand_base_width + sloped_caissons_concrete_filled_with_sand_number_of_units * sloped_caissons_concrete_filled_with_sand_base_width  #E98 #='=E84*E86+E73*E75
    intermediate_caisson_walls_top_width = caisson_cap_width  #E99 #='=E105
    #intermediate_caisson_walls_wall_thickness #E100 #if ('=IF(E$15<30,0.5,0.75)
    if ( caisson_breakwater_height < 30.0) :
        intermediate_caisson_walls_wall_thickness  = 0.5
    else :
        intermediate_caisson_walls_wall_thickness  = 0.75
    intermediate_caisson_walls_volume_concrete = intermediate_caisson_walls_number_of_units * intermediate_caisson_walls_height * (( intermediate_caisson_walls_base_width + intermediate_caisson_walls_top_width ) / 2.0) * intermediate_caisson_walls_wall_thickness  #E101 #='=E96*E97*(E98+E99)/2*E100

    # caisson_cap
    caisson_cap_height = 2.0  #E104 #=2
    caisson_cap_length = caisson_breakwater_length  #E106 #='=E$14
    caisson_cap_volume_concrete = caisson_cap_height * caisson_cap_width * caisson_cap_length  #E107 #='=E104*E105*E106

    # caisson_cap_seaside_parapet_wall
    caisson_cap_seaside_parapet_wall_height = freeboard  #E110 #='=E28
    caisson_cap_seaside_parapet_wall_width = caisson_cap_seaside_parapet_wall_height / 2.0  #E111 #='=E110/2
    caisson_cap_seaside_parapet_wall_length = caisson_breakwater_length  #E112 #='=E$14
    caisson_cap_seaside_parapet_wall_volume_concrete = caisson_cap_seaside_parapet_wall_height * caisson_cap_seaside_parapet_wall_width * caisson_cap_seaside_parapet_wall_length  #E113 #='=E110*E111*E112

    # leeside_mass_concrete_block
    leeside_mass_concrete_block_length = caisson_breakwater_length  #E119 #='=E$14
    leeside_mass_concrete_block_volume = leeside_mass_concrete_block_number_of_units * leeside_mass_concrete_block_height * leeside_mass_concrete_block_width * leeside_mass_concrete_block_length  #E120 #='=E116*E117*E118*E119

    # leeside_armor_berm_large_riprap
    leeside_armor_berm_large_riprap_width_total = leeside_armor_berm_large_riprap_width_sloped + leeside_armor_berm_large_riprap_width_toe + leeside_armor_berm_large_riprap_width_top  #E128 #='=E127+E124+E126
    leeside_armor_berm_large_riprap_length = caisson_breakwater_length  #E129 #='=E$14
    leeside_armor_berm_large_riprap_volume = leeside_armor_berm_large_riprap_depth * leeside_armor_berm_large_riprap_width_total * leeside_armor_berm_large_riprap_length  #E130 #='=E123*E128*E129


    # Rubble Breakwater (Mound), parameters
    #Moved up to resolve conflicts
    #filter_toe_berm_gravel_seaside_depth #E153 #if (IF(E$13<8;1;2)
    if ( rubble_breakwater_height < 8.0 ) :
        filter_toe_berm_gravel_seaside_depth = 1.0
    else :
        filter_toe_berm_gravel_seaside_depth = 2.0

    #secondary_armor_toe_small_riprap_seaside_depth #E167 #if (IF(E$13<8;1.5;2)
    if ( rubble_breakwater_height < 8.0 ) :
        secondary_armor_toe_small_riprap_seaside_depth = 1.5
    else :
        secondary_armor_toe_small_riprap_seaside_depth = 2.0
    granular_filter_gravel_depth = 0.5  #E160 #=0.5

    #secondary_armor_small_riprap_depth #E174 #if (IF(E$13<8;1;1.5)
    if ( rubble_breakwater_height < 8.0 ) :
        secondary_armor_small_riprap_depth = 1.0
    else :
        secondary_armor_small_riprap_depth = 1.5
    primary_armor_large_riprap_depth = 2.0  #E180 #=2
    primary_armor_large_riprap_width_crest = 8.0  #E181 #=8
    secondary_armor_toe_small_riprap_seaside_width_exposed = 3.0  #E168 #=3

    freeboard = 0.6  #E133 #=0.6
    minimum_height = filter_toe_berm_gravel_seaside_depth + secondary_armor_toe_small_riprap_seaside_depth + granular_filter_gravel_depth + secondary_armor_small_riprap_depth + primary_armor_large_riprap_depth + freeboard  #E134 #=SUM(E153;E167;E160;E174;E180;E133)
    design_height = max( rubble_breakwater_height , minimum_height )  #E135 #=MAX(E13;E134)
    seaside_slope = 1.5  #E136 #=1.5
    leeside_slope = 1.5  #E137 #=1.5

    #Moved up to resolve conflicts
    core_quarry_run_stone_width_top = primary_armor_large_riprap_width_crest  #E148 #=E181
    core_quarry_run_stone_height = design_height - granular_filter_gravel_depth - secondary_armor_small_riprap_depth - primary_armor_large_riprap_depth  #E146 #=E135-E160-E174-E180
    core_quarry_run_stone_width_base = ( 2.0 * core_quarry_run_stone_height * seaside_slope ) + core_quarry_run_stone_width_top  #E147 #=2*E146*E136+E148
    granular_filter_gravel_height = core_quarry_run_stone_height + granular_filter_gravel_depth  #E161 #=E146+E160
    granular_filter_gravel_total_cross_sectional_length = granular_filter_gravel_height * seaside_slope * 2.0 + core_quarry_run_stone_width_top  #E162 #=E161*E136*2+E148

    #dredge_and_replace_with_quarry_run_stone
    dredge_and_replace_with_quarry_run_stone_depth = 1.0  #E140 #=1
    dredge_and_replace_with_quarry_run_stone_width = core_quarry_run_stone_width_base + ( 2.0 * granular_filter_gravel_total_cross_sectional_length )  #E141 #=E147+2*E162
    dredge_and_replace_with_quarry_run_stone_length = rubble_breakwater_length  #E142 #=E$12
    dredge_and_replace_with_quarry_run_stone_volume = dredge_and_replace_with_quarry_run_stone_depth * dredge_and_replace_with_quarry_run_stone_width * dredge_and_replace_with_quarry_run_stone_length  #E143 #=E140*E141*E142

    #core_quarry_run_stone
    core_quarry_run_stone_length = rubble_breakwater_length  #E149 #=E$12
    core_quarry_run_stone_volume = 0.5 * core_quarry_run_stone_height * ( core_quarry_run_stone_width_base + core_quarry_run_stone_width_top ) * core_quarry_run_stone_length  #E150 #=0.5*E146*(E147+E148)*E149

    #filter_toe_berm_gravel_seaside
    filter_toe_berm_gravel_seaside_width_exposed = 1.5  #E154 #=1.5
    filter_toe_berm_gravel_seaside_width_total = filter_toe_berm_gravel_seaside_width_exposed + secondary_armor_toe_small_riprap_seaside_width_exposed + primary_armor_large_riprap_depth + secondary_armor_small_riprap_depth  #E155 #=E154+E168+E180+E174
    filter_toe_berm_gravel_seaside_length = rubble_breakwater_length  #E156 #=E$12
    filter_toe_berm_gravel_seaside_volume = filter_toe_berm_gravel_seaside_depth * filter_toe_berm_gravel_seaside_width_total * filter_toe_berm_gravel_seaside_length  #E157 #=E153*E155*E156

    #granular_filter_gravel
    granular_filter_gravel_length = rubble_breakwater_length  #E163 #=E$12
    granular_filter_gravel_volume = granular_filter_gravel_depth * granular_filter_gravel_total_cross_sectional_length * granular_filter_gravel_length #E164 #=E160*E162*E163

    #secondary_armor_toe_small_riprap_seaside
    secondary_armor_toe_small_riprap_seaside_width_total = secondary_armor_toe_small_riprap_seaside_width_exposed + ( 2.0 * secondary_armor_toe_small_riprap_seaside_depth * seaside_slope )  #E169 #=E168+2*E167*E136
    secondary_armor_toe_small_riprap_seaside_length = rubble_breakwater_length  #E170 #=E$12
    secondary_armor_toe_small_riprap_seaside_volume = secondary_armor_toe_small_riprap_seaside_length * secondary_armor_toe_small_riprap_seaside_depth * ( secondary_armor_toe_small_riprap_seaside_width_exposed + secondary_armor_toe_small_riprap_seaside_width_total ) / 2.0  #E171 #=E170*E167*(E168+E169)/2

    #secondary_armor_small_riprap
    secondary_armor_small_riprap_width = core_quarry_run_stone_width_top + ( secondary_armor_toe_small_riprap_seaside_depth + design_height - minimum_height + granular_filter_gravel_depth ) * seaside_slope  #E175 #=E148+(E167+E135-E134+E160)*E136
    secondary_armor_small_riprap_length = rubble_breakwater_length  #E176 #=E$12
    secondary_armor_small_riprap_volume = secondary_armor_small_riprap_depth * secondary_armor_small_riprap_width * secondary_armor_small_riprap_length  #E177 #=E174*E175*E176

    #primary_armor_large_riprap
    primary_armor_large_riprap_height_seaside = rubble_breakwater_height - filter_toe_berm_gravel_seaside_depth  #E182 #=E13-E153
    primary_armor_large_riprap_height_leeside = min( 3.0 * ( primary_armor_large_riprap_depth + secondary_armor_small_riprap_depth + granular_filter_gravel_depth ), primary_armor_large_riprap_height_seaside )  #E183 #=MIN(3*(E180+E174+E160);E182)
    primary_armor_large_riprap_length = rubble_breakwater_length  #E184 #=E$12
    primary_armor_large_riprap_volume = primary_armor_large_riprap_length * ( primary_armor_large_riprap_depth * primary_armor_large_riprap_width_crest + primary_armor_large_riprap_depth * math.sqrt( pow(primary_armor_large_riprap_height_seaside, 2.0) + pow(( primary_armor_large_riprap_height_seaside * seaside_slope ), 2.0))+ primary_armor_large_riprap_depth * math.sqrt( pow(primary_armor_large_riprap_height_leeside, 2.0) + pow(( primary_armor_large_riprap_height_leeside * leeside_slope ), 2.0)))  #E185 #=E184*(E180*E181+E180*SQRT(E182^2+(E182*E136)^2)+E180*SQRT(E183^2+(E183*E137)^2))

    #secondary_armor_toe_small_riprap_leeside
    if ( rubble_breakwater_height < 8.0 ) :
        secondary_armor_toe_small_riprap_leeside_depth = 1.5
    else :
        secondary_armor_toe_small_riprap_leeside_depth = 2.0  #E188 #if (IF(E$13<8;1.5;2)
    secondary_armor_toe_small_riprap_leeside_width_exposed = 3.0  #E189 #=3
    secondary_armor_toe_small_riprap_leeside_width_total = secondary_armor_toe_small_riprap_leeside_width_exposed + 2.0 * secondary_armor_toe_small_riprap_leeside_depth * leeside_slope  #E190 #=E189+2*E188*E137
    secondary_armor_toe_small_riprap_leeside_length = rubble_breakwater_length  #E191 #=E$12
    secondary_armor_toe_small_riprap_leeside_volume = secondary_armor_toe_small_riprap_leeside_length * secondary_armor_toe_small_riprap_leeside_depth * ( secondary_armor_toe_small_riprap_leeside_width_exposed + secondary_armor_toe_small_riprap_leeside_width_total ) / 2.0  #E192 #=E191*E188*(E189+E190)/2

    #filter_toe_berm_gravel_leeside
    if ( rubble_breakwater_height < 8.0 ) :
        filter_toe_berm_gravel_leeside_depth = 1.0
    else :
        filter_toe_berm_gravel_leeside_depth = 2.0  #E195 #if (IF(E$13<8;1;2)
    filter_toe_berm_gravel_leeside_width_exposed = 1.5  #E196 #=1.5
    filter_toe_berm_gravel_leeside_width_total = filter_toe_berm_gravel_leeside_width_exposed + secondary_armor_toe_small_riprap_leeside_width_exposed * ( 1.0 + secondary_armor_toe_small_riprap_leeside_width_exposed * leeside_slope ) + secondary_armor_toe_small_riprap_seaside_depth + primary_armor_large_riprap_depth  #E197 #=E196+E189*(1+E189*E137)+E167+E180
    filter_toe_berm_gravel_leeside_length = rubble_breakwater_length  #E198 #=E$12
    filter_toe_berm_gravel_leeside_volume = filter_toe_berm_gravel_leeside_depth * filter_toe_berm_gravel_leeside_width_exposed * filter_toe_berm_gravel_leeside_length  #E199 #=E195*E196*E198



    # Flood Wall, parameters
    #Moved up to resolve conflicts
    wall_stem_height = cantilever_floodwall_height  #E248 #=E11
    base_slab_width = wall_stem_height  #E225 #=E248
    stabilization_slab_height = 0.5  #E215 #=0.5

    freeboard = 0.9  #E203 #=0.9
    minimum_wall_stem_height = 2.0  #E204 #=2
    maximum_wall_stem_height = 10.0  #E205 #=10
    #design_wall_stem_height #E206 #=IF(E11>E204;IF(E11<E205;E11;E205);E204)
    if ( cantilever_floodwall_height > minimum_wall_stem_height ) :
        if ( cantilever_floodwall_height < maximum_wall_stem_height ) :
            design_wall_stem_height = cantilever_floodwall_height
        else :
            design_wall_stem_height = maximum_wall_stem_height
    else :
        design_wall_stem_height = minimum_wall_stem_height

    #excavate_and_replace_with_compacted_gravel
    excavate_and_replace_with_compacted_gravel_depth = 1.0  #E209 #=1
    excavate_and_replace_with_compacted_gravel_width = base_slab_width + 2.0 * stabilization_slab_height  #E210 #=E225+2*E215
    excavate_and_replace_with_compacted_gravel_length = cantilever_floodwall_length  #E211 #=E$10
    excavate_and_replace_with_compacted_gravel_volume_of_gravel = excavate_and_replace_with_compacted_gravel_depth * excavate_and_replace_with_compacted_gravel_width * excavate_and_replace_with_compacted_gravel_length  #E212 #=E209*E210*E211

    #stabilization_slab
    stabilization_slab_width = base_slab_width + 2.0  #E216 #=E225+2
    stabilization_slab_length = cantilever_floodwall_length  #E217 #=E$10
    stabilization_slab_volume_of_concrete = stabilization_slab_height * stabilization_slab_width * stabilization_slab_length  #E218 #=E215*E216*E217
    stabilization_slab_concrete_to_rebar_volumetric_ratio = 1.0  #E219 #=1
    stabilization_slab_volume_of_reinforcing_steel = stabilization_slab_concrete_to_rebar_volumetric_ratio / 100 * stabilization_slab_volume_of_concrete  #E220 #=E219/100*E218
    stabilization_slab_mass_of_reinforcing_steel = stabilization_slab_volume_of_reinforcing_steel * density_of_steel  #E221 #=E220*$LUTs.D$3

    #base_slab
    if ( design_wall_stem_height < 4.0 ) :
        base_slab_depth = 1.0
    else :
        base_slab_depth = 1.5  #E224 #if (IF(E206<4;1;1.5)
    base_slab_heel_width = base_slab_width / 4.0 * 3.0  #E226 #=E225/4*3
    base_slab_toe_width = base_slab_width / 4.0  #E227 #=E225/4
    base_slab_length = cantilever_floodwall_length  #E228 #=E$10
    base_slab_volume_of_concrete = base_slab_depth * base_slab_width * base_slab_length  #E229 #=E224*E225*E228
    base_slab_concrete_to_rebar_volumetric_ratio = 2.0  #E230 #=2
    base_slab_volume_of_reinforcing_steel = base_slab_concrete_to_rebar_volumetric_ratio / 100.0 * base_slab_volume_of_concrete  #E231 #=E230/100*E229
    base_slab_mass_of_reinforcing_steel = base_slab_volume_of_reinforcing_steel * density_of_steel  #E232 #=E231*$LUTs.D$3
    base_slab_seepage_cutoff_sheet_pile_wall_depth = min( 2.0 * design_wall_stem_height , 31.0 )  #E233 #=MIN(2*E206;31)
    base_slab_volume_of_sheet_pile_steel = 0.000165 * base_slab_length * base_slab_seepage_cutoff_sheet_pile_wall_depth  #E234 #=0.000165*E228*E233
    base_slab_mass_of_sheet_pile_steel = base_slab_volume_of_sheet_pile_steel * density_of_steel  #E235 #=E234*$LUTs.D$3

    #h_pile_supports
    h_pile_supports_depth_below_ground_surface = design_wall_stem_height * 5.0  #E238 #=5*E206
    h_pile_supports_slope = 3.0  #E239 #=3
    h_pile_supports_length = math.sqrt(  pow( h_pile_supports_depth_below_ground_surface, 2.0) + pow(( h_pile_supports_depth_below_ground_surface / h_pile_supports_slope ), 2.0))  #E240 #=SQRT(E238^2+(E238/E239)^2)

    #h_pile_supports_size #E241 #=IF(E206<4;"10x57";IF(E206>7;"14x102";"12x74"))
    if ( design_wall_stem_height < 4.0 ) :
        h_pile_supports_size = "10x57"
    elif ( design_wall_stem_height > 7.0 ) :
        h_pile_supports_size = "14x102"
    else :
        h_pile_supports_size = "12x74"

    h_pile_supports_spacing = 3.0  #E242 #=3
    #h_pile_supports_no_of_piles_at_each_spacing_interval #E243 #if (IF(E225>5;3;2)
    if ( base_slab_width > 5.0 ) :
        h_pile_supports_no_of_piles_at_each_spacing_interval = 3.0
    else :
        h_pile_supports_no_of_piles_at_each_spacing_interval = 2.0

    if ( h_pile_supports_size == "10x57" ) :
        h_pile_supports_volume_of_steel = 16.8
    elif ( h_pile_supports_size == "14x117" ) :
        h_pile_supports_volume_of_steel = 30.0
    else :
        h_pile_supports_volume_of_steel = 21.8
    h_pile_supports_volume_of_steel = h_pile_supports_volume_of_steel * 0.00064516 * h_pile_supports_length * cantilever_floodwall_length / h_pile_supports_spacing * h_pile_supports_no_of_piles_at_each_spacing_interval  #E244 #=IF(E241="10x57";16.8;IF(E241="14x117";30;21.8))*0.00064516*E240*E$10/E242*E243

    h_pile_supports_mass_of_reinforcing_steel = h_pile_supports_volume_of_steel * density_of_steel  #E245 #=E244*$LUTs.D$3

    #wall_stem
    wall_stem_width_stem_top = 2.0  #E249 #=2
    if ( design_wall_stem_height > 7.0 ) :
        wall_stem_width_stem_bottom = wall_stem_width_stem_top * 1.5
    else :
        wall_stem_width_stem_bottom = wall_stem_width_stem_top  #E250 #if (IF(E206>7;E249*1.5;E249)
    wall_stem_length = cantilever_floodwall_length  #E251 #=E$10
    wall_stem_volume_of_concrete = ( wall_stem_width_stem_top + wall_stem_width_stem_bottom ) * wall_stem_height * wall_stem_length / 2.0  #E252 #=(E249+E250)*E248*E251/2
    wall_stem_concrete_to_rebar_volumetric_ratio = 1.5  #E253 #=1.5
    wall_stem_volume_of_reinforcing_steel = wall_stem_concrete_to_rebar_volumetric_ratio / 100.0 * wall_stem_volume_of_concrete  #E254 #=E253/100*E252
    wall_stem_mass_of_reinforcing_steel = wall_stem_volume_of_reinforcing_steel * density_of_steel  #E255 #=E254*$LUTs.D$3




    #CONSTRUCTION MATERIALS SUMMARY
    sand =  sloped_caissons_concrete_filled_with_sand_volume_sand + rectangular_caissons_concrete_filled_with_sand_volume_sand #m^3 =SUM(E81;E91)
    gravel = leveling_course_gravel_volume + filter_toe_berm_gravel_seaside_volume + granular_filter_gravel_volume + filter_toe_berm_gravel_leeside_volume + excavate_and_replace_with_compacted_gravel_volume_of_gravel #m^3 =SUM(E63;E157;E164;E199;E212)
    quarry_run_stone =  dredge_and_replace_with_quarry_run_stone_volume_caisson + core_quarry_run_stone_volume_caisson + dredge_and_replace_with_quarry_run_stone_volume + core_quarry_run_stone_volume #m^3 =SUM(E34;E40;E143;E150)
    large_riprap = primary_armor_berm_large_riprap_volume + leeside_armor_berm_large_riprap_volume + primary_armor_large_riprap_volume #m^3 =SUM(E57;E130;E185)
    small_riprap = scour_blanket_toe_berm_small_riprap_volume + secondary_armor_toe_small_riprap_seaside_volume + secondary_armor_small_riprap_volume + secondary_armor_toe_small_riprap_leeside_volume #m^3 =SUM(E47;E171;E177;E192)
    concrete = primary_mass_concrete_block_volume + sloped_caissons_concrete_filled_with_sand_volume_concrete + rectangular_caissons_concrete_filled_with_sand_volume_concrete + intermediate_caisson_walls_volume_concrete + caisson_cap_volume_concrete + leeside_mass_concrete_block_volume + stabilization_slab_volume_of_concrete + base_slab_volume_of_concrete + wall_stem_volume_of_concrete #m^3 =SUM(E70;E80;E90;E101;E107;E120;E218;E229;E252)
    structural_steel = ( stabilization_slab_mass_of_reinforcing_steel + base_slab_mass_of_reinforcing_steel + base_slab_mass_of_sheet_pile_steel + h_pile_supports_mass_of_reinforcing_steel + wall_stem_mass_of_reinforcing_steel ) / 1000 #tonv =SUM(E221;E232;E235;E245;E255)/1000

    structural_steel_volume = (structural_steel * 1000 / density_of_steel)

    #TODO: update return function and value weighting function
    toeVolume = 1;
    coreVolume = 1;
    dikeVolume = 1;
    foundVolume = 1;
    armorVolume = 1;

    # for purposes of the algorithm, the dike volume can proxy for the cost
    return {
               'structure_type': structure_type,
               'sand_volume': sand,
               'gravel_volume': gravel,
               'quarry_run_stone_volume': quarry_run_stone,
               'large_riprap_volume': large_riprap,
               'small_riprap_volume': small_riprap,
               'concrete_volume': concrete,
               'structural_steel_weight': structural_steel,
               'structural_steel_volume': structural_steel_volume,
               'structure_height_above_msl': elev_no_structure_needed,

               'toeVol': toeVolume,
               'elev': elev,
               'length': length,
               'coreVol' : coreVolume,
               'dikeVol' : dikeVolume,
               'foundVol' : foundVolume,
               'armorVol' : armorVolume,

               # cost for optimization is total volume of material in m^3
               'cost' : sand + gravel + quarry_run_stone + large_riprap + small_riprap + concrete + structural_steel_volume + no_structure_needed_optimization_cost
            }
