export default async function GetUserPassword() {
  try {
    // Check if we're running locally
    const isLocal = typeof window !== 'undefined' && (
      window.location.hostname === 'localhost' ||
      window.location.hostname === '127.0.0.1'
    );

    // Use local URL when running locally, public URL otherwise
    const backendUrl = isLocal
      ? process.env.NEXT_PUBLIC_BACKEND_LOCAL
      : process.env.NEXT_PUBLIC_BACKEND_PUBLIC;

    console.log("Using backend URL:", backendUrl);

    const response = await fetch(`${backendUrl}/api/user-password`, {
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