export default async function LoginUser(username: string, password: string) {
  try {
    // Create authentication token
    const authToken = btoa(`${username}:${password}`);
    
    // Store in both localStorage (for API calls) and cookies (for middleware)
    if (typeof window !== 'undefined') {
      localStorage.setItem('authToken', authToken);
      
      // Set a cookie with the auth token
      document.cookie = `authToken=${authToken}; path=/; max-age=86400; secure`;
    }

    // Try authentication against API
    const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_LOCAL}/api/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Basic ${authToken}`
      }
    });
    
    if (!response.ok) {
      // Clear storage if authentication failed
      localStorage.removeItem('authToken');
      document.cookie = 'authToken=; path=/; max-age=0';
      return { error: true, message: 'You do not have permission' };
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Login error:", error);
    return { 
      error: true, 
      message: error instanceof Error ? error.message : 'Error connecting to server' 
    };
  }
}