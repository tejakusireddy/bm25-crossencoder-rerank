def flow_pipeminor(Diam, HeadLossExpans, KMinor):
    
    #Checking input validity - inputs not checked here are checked by
    #functions this function calls.
    ut.check_range([HeadLossExpans, ">=0", "Headloss due to expansion"],
                   [KMinor, ">0", "K minor"])
    return (area_circle(Diam).magnitude * np.sqrt(2 * gravity.magnitude
                                                  * HeadLossExpans
                                                  / KMinor)
            )