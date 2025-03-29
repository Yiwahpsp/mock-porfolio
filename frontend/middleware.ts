import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Get stored auth token from cookies
  const authToken = request.cookies.get('authToken')?.value;
  
  // Check if user is accessing protected routes
  const isAdminRoute = request.nextUrl.pathname.startsWith('/admin/dashboard');
  const isLoginPage = request.nextUrl.pathname === '/admin';
  
  // If trying to access protected route without auth
  if (isAdminRoute && !authToken) {
    // Redirect to login
    return NextResponse.redirect(new URL('/admin', request.url));
  }
  
  // If already logged in and trying to access login page
  if (isLoginPage && authToken) {
    // Redirect to dashboard
    return NextResponse.redirect(new URL('/admin/dashboard', request.url));
  }
  
  return NextResponse.next();
}

// Specify which routes this middleware applies to
export const config = {
  matcher: ['/admin/:path*']
};