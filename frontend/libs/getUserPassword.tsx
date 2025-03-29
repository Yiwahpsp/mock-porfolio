export default async function GetUserPassword() {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_PUBLIC}/api/user-password`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    const data = await response.json();
    return data;
  } catch (error) {
    throw new Error('Error deleting user data:', error || "cannot connect to server");
  };
}