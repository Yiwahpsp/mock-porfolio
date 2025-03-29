export default async function ProtectedAdmin(token: string) {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_PUBLIC}/api/protected`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Basic ${token}`,
      },
      credentials: 'include',
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Unauthorized. Please log in again.');
      }
      throw new Error(`Failed to fetch protected admin data: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    throw new Error('Error fetching protected admin data:', error || "cannot connect to server");
  }
}