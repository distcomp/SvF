def pw_xt_val(xVals, scaled_t: float, Nt):
    """
    Get value of piecewise X(t) for arbitrary scaled (!) t \in [0, Nt]
    :param scaled_t: scaled t
    :param Nt: number of segments over t
    :return: pyo Expression !
    """
    if scaled_t < 0 or scaled_t > Nt:
        raise Exception("pw_xt_val: scaled_t (%f) IS NOT IN [0, %d]" %(scaled_t, Nt))
    k = int(scaled_t)
    return (xVals[k]*(k + 1 - scaled_t) + xVals[min(k+1,Nt)]*(scaled_t - k))

if __name__ == "__main__":
    # print(str(testYield()))
    # print(str(testYield()))
    xVals = [1, 2, 3, 4, 5, 6]
    for t in (0., 0.5, 1., 1.5, 2.5, 3.5, 4., 4.3, 5.):
        print('t = %f, x = %f' % (t, pw_xt_val(xVals, t, 5)) )


    quit()
