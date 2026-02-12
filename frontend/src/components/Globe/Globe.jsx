import React, { useRef, useEffect, useState, useMemo } from 'react';
import GlobeGL from 'react-globe.gl';
import { COUNTRY_COORDINATES } from '../../data/countryCoordinates';
import './Globe.css';

const Globe = ({ fromCountry, toCountry, showArc, mini = false }) => {
  const globeRef = useRef();
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });
  const containerRef = useRef();

  // Update dimensions on mount and resize
  useEffect(() => {
    const updateDimensions = () => {
      if (containerRef.current) {
        const { width, height } = containerRef.current.getBoundingClientRect();
        setDimensions({ width, height });
      }
    };

    updateDimensions();
    window.addEventListener('resize', updateDimensions);
    return () => window.removeEventListener('resize', updateDimensions);
  }, []);

  // Initialize auto-rotation after globe renders
  useEffect(() => {
    const timer = setTimeout(() => {
      if (globeRef.current) {
        const controls = globeRef.current.controls();
        if (controls) {
          controls.autoRotate = true;
          controls.autoRotateSpeed = mini ? 1.5 : 0.5;
        }
      }
    }, 100);
    return () => clearTimeout(timer);
  }, [dimensions.width, mini]);

  // Control auto-rotation based on country selection
  useEffect(() => {
    if (globeRef.current) {
      const controls = globeRef.current.controls();
      if (controls) {
        // Mini globe always rotates, main globe stops when country selected
        controls.autoRotate = mini || !fromCountry || fromCountry === '';
        controls.autoRotateSpeed = mini ? 1.5 : 0.5;
      }
    }
  }, [fromCountry, mini]);

  // Animate camera to focus on selected country
  useEffect(() => {
    if (globeRef.current && fromCountry && COUNTRY_COORDINATES[fromCountry]) {
      const coords = COUNTRY_COORDINATES[fromCountry];
      globeRef.current.pointOfView(
        { lat: coords.lat, lng: coords.lng, altitude: mini ? 2.5 : 1.8 },
        1000
      );
    }
  }, [fromCountry, mini]);

  // Generate pins data based on selected countries
  const pinsData = useMemo(() => {
    const pins = [];

    if (fromCountry && COUNTRY_COORDINATES[fromCountry]) {
      pins.push({
        lat: COUNTRY_COORDINATES[fromCountry].lat,
        lng: COUNTRY_COORDINATES[fromCountry].lng,
        color: '#ACC8A2', // Soft sage for source
        name: COUNTRY_COORDINATES[fromCountry].name,
        type: 'source'
      });
    }

    if (toCountry && COUNTRY_COORDINATES[toCountry] && toCountry !== fromCountry) {
      pins.push({
        lat: COUNTRY_COORDINATES[toCountry].lat,
        lng: COUNTRY_COORDINATES[toCountry].lng,
        color: '#4CAF50', // Green for destination
        name: COUNTRY_COORDINATES[toCountry].name,
        type: 'destination'
      });
    }

    return pins;
  }, [fromCountry, toCountry]);

  // Generate arc data for the connection line
  const arcData = useMemo(() => {
    if (showArc && fromCountry && toCountry &&
        COUNTRY_COORDINATES[fromCountry] && COUNTRY_COORDINATES[toCountry] &&
        fromCountry !== toCountry) {
      return [{
        startLat: COUNTRY_COORDINATES[fromCountry].lat,
        startLng: COUNTRY_COORDINATES[fromCountry].lng,
        endLat: COUNTRY_COORDINATES[toCountry].lat,
        endLng: COUNTRY_COORDINATES[toCountry].lng,
        color: ['#ACC8A2', '#4CAF50']
      }];
    }
    return [];
  }, [showArc, fromCountry, toCountry]);

  return (
    <div
      ref={containerRef}
      className={`globe-container ${mini ? 'globe-mini' : ''}`}
    >
      {dimensions.width > 0 && (
        <GlobeGL
          ref={globeRef}
          width={dimensions.width}
          height={dimensions.height}
          globeImageUrl="//unpkg.com/three-globe/example/img/earth-blue-marble.jpg"
          backgroundColor="rgba(0,0,0,0)"

          // Pins
          pointsData={mini ? [] : pinsData}
          pointLat="lat"
          pointLng="lng"
          pointColor="color"
          pointAltitude={0.15}
          pointRadius={0.6}
          pointLabel="name"

          // Arcs
          arcsData={arcData}
          arcStartLat="startLat"
          arcStartLng="startLng"
          arcEndLat="endLat"
          arcEndLng="endLng"
          arcColor="color"
          arcDashLength={0.4}
          arcDashGap={0.2}
          arcDashAnimateTime={2000}
          arcStroke={0.5}

          // Atmosphere
          atmosphereColor="#ACC8A2"
          atmosphereAltitude={0.15}
        />
      )}
    </div>
  );
};

export default Globe;
