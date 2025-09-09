import fs from 'fs';
import path from 'path';

// Define file paths for GeoJSON data
const geoJsonDir = path.resolve(process.cwd());
const adminDataPath = path.join(geoJsonDir, 'geoBoundaries-AFG-ADM2_risk.geojson');
const roadDataPath = path.join(geoJsonDir, 'access_map_yesterday.geojson');

export async function handler(event, context) {
  try {
    // Read GeoJSON files
    const adminData = JSON.parse(fs.readFileSync(adminDataPath, 'utf8'));
    const roadData = JSON.parse(fs.readFileSync(roadDataPath, 'utf8'));

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*' // Enable CORS
      },
      body: JSON.stringify({ adminData, roadData })
    };
  } catch (error) {
    console.error('Function error:', error);
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ error: 'Failed to load GeoJSON data' })
    };
  }
}