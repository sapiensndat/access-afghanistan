export async function handler(event, context) {
  // Example JSON response for dashboard
  const data = {
    message: "Dashboard data loaded",
    coordinates: [
      { lat: -2.331341, lng: 28.878772 },
      { lat: -2.330000, lng: 28.880380 }
    ]
  };

  return {
    statusCode: 200,
    body: JSON.stringify(data),
    headers: { "Content-Type": "application/json" }
  };
}