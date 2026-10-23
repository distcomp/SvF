
import SurMin as sm

def get_sigCV( Penal ):
    print (Penal)
    return (Penal[0]-1)**2

def main():
    ints, step = sm.SurMin ( 30, [0.0001], 1e-5, [0.5], get_sigCV, '/opt/scipopt911/bin/ipopt'  )
   # print (ints, step)

if __name__ == "__main__":
    main()

