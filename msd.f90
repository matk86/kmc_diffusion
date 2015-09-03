subroutine compute(t, x, y, z, dt, dx2, dy2, dz2, n)
  integer n, i
  real :: x(n), y(n), z(n), t(n)   
  real :: dx2(n), dy2(n), dz2(n), dt(n) 

 !f2py intent(in) n
 !f2py intent(in) t  
 !f2py intent(in) x
 !f2py intent(in) y
 !f2py intent(in) z
  
 !f2py intent(in,out) dt
 !f2py intent(in,out) dx2
 !f2py intent(in,out) dy2
 !f2py intent(in,out) dz2  

 !f2py depend(n) t  
 !f2py depend(n) x
 !f2py depend(n) y
 !f2py depend(n) z
 !f2py depend(n) dt
 !f2py depend(n) dx2
 !f2py depend(n) dy2
 !f2py depend(n) dz2

  do i=1,n-1
     dt(i) = sum(t(i:n) - t(1:n-i) )/(n-i)
     dx2(i) = sum(( x(i:n) - x(1:n-i) )**2)/(n-i)
     dy2(i) = sum(( y(i:n) - y(1:n-i) )**2)/(n-i)
     dz2(i) = sum(( z(i:n) - z(1:n-i) )**2)/(n-i)
  enddo
  
end subroutine compute

