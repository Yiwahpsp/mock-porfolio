export default async function GetUserPassword() {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_LOCAL}/api/user-password`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch user password');
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    throw new Error('Error fetching user password:', error || "cannot connect to server");
  }
}