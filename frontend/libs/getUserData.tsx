export default async function GetUserData(token: string) {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_PUBLIC}/api/user-data`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Basic ${token}`,
      }
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Unauthorized. Please log in again.');
      }
      throw new Error(`Failed to delete user data: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    throw new Error('Error fetching user data:', error || "cannot connect to server");
  }
}