def __hilbert(x0, y0, xi, xj, yi, yj, n):
    points=[]
    if n <= 0:
        X = x0 + (xi + yi)/2
        Y = y0 + (xj + yj)/2
        return [X, Y]
    else:
        points.extend(__hilbert(x0,               y0,               yi/2, yj/2, xi/2, xj/2, n - 1))
        points.extend(__hilbert(x0 + xi/2,        y0 + xj/2,        xi/2, xj/2, yi/2, yj/2, n - 1))
        points.extend(__hilbert(x0 + xi/2 + yi/2, y0 + xj/2 + yj/2, xi/2, xj/2, yi/2, yj/2, n - 1))
        points.extend(__hilbert(x0 + xi/2 + yi,   y0 + xj/2 + yj,  -yi/2,-yj/2,-xi/2,-xj/2, n - 1))
        return points

def hilbert(x0,y0,xi,xj,yi,yj,n):
    coords = __hilbert(x0,y0,xi,xj,yi,yj,n)
    new_coords = [[coords[i], coords[i+1]] for i in range(0,len(coords),2)]
    return new_coords
        
def create_hilbert(n):
    return [[int(i[0]), int(i[1])] for i in hilbert(0,0,2**n,0,0,2**n,n)]
