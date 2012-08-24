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
    
    # for purposes of the algorithm, the dike volume can proxy for the cost
    return {   'toeVol': toeVolume,
                'coreVol' : coreVolume,
                'dikeVol' : dikeVolume,
                'foundVol' : foundVolume,
                'armorVol' : armorVolume,
                'cost' : dikeVolume + coreVolume + toeVolume + foundVolume + armorVolume
            }
