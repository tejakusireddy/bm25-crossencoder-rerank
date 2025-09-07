def box_actions(results, times, N_matrix, ifprint):
    
    if(ifprint):
        print("\n=====\nUsing triaxial harmonic toy potential")

    t = time.time()
    # Find best toy parameters
    omega = toy.findbestparams_ho(results)
    if(ifprint):
        print("Best omega "+str(omega)+" found in "+str(time.time()-t)+" seconds")

    # Now find toy actions and angles
    AA = np.array([toy.angact_ho(i,omega) for i in results])
    AA = AA[~np.isnan(AA).any(1)]
    if(len(AA)==0):
        return

    t = time.time()
    act = solver.solver(AA, N_matrix)
    if act==None:
        return

    if(ifprint):
        print("Action solution found for N_max = "+str(N_matrix)+", size "+str(len(act[0]))+" symmetric matrix in "+str(time.time()-t)+" seconds")

    np.savetxt("GF.Sn_box",np.vstack((act[1].T,act[0][3:])).T)

    ang = solver.angle_solver(AA,times,N_matrix,np.ones(3))
    if(ifprint):
        print("Angle solution found for N_max = "+str(N_matrix)+", size "+str(len(ang))+" symmetric matrix in "+str(time.time()-t)+" seconds")

    # Just some checks
    if(len(ang)>len(AA)):
        print("More unknowns than equations")

    return act[0], ang, act[1], AA, omega