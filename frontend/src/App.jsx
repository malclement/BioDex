import { useState, useRef } from 'react'
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
import './App.css'
import SidePanel from './SidePanel'

// Fix for missing marker icons
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: new URL('leaflet/dist/images/marker-icon-2x.png', import.meta.url).href,
  iconUrl: new URL('leaflet/dist/images/marker-icon.png', import.meta.url).href,
  shadowUrl: new URL('leaflet/dist/images/marker-shadow.png', import.meta.url).href,
})

// Custom colored marker icon
const createCustomIcon = (color = 'blue') => {
  return new L.Icon({
    iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-${color}.png`,
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  })
}

// Component to handle map clicks
function MapClickHandler({ onMapClick, isPlacingMarker }) {
  useMapEvents({
    click: (e) => {
      if (isPlacingMarker) {
        onMapClick(e.latlng)
      }
    }
  })
  return null
}

export default function App() {
  const [markers, setMarkers] = useState([])
  const [isPlacingMarker, setIsPlacingMarker] = useState(false)
  const [activeMarker, setActiveMarker] = useState(null)
  const [savingMarkers, setSavingMarkers] = useState({}) // Track markers being saved
  const [notification, setNotification] = useState(null)
  const mapRef = useRef(null)

  // Show notification helper
  const showNotification = (message, type = 'info') => {
    setNotification({ message, type });

    // Auto-dismiss after 3 seconds
    setTimeout(() => {
      setNotification(null);
    }, 3000);
  }

  const handleMapClick = (latlng) => {
    const newMarker = {
      id: Date.now(), // Use timestamp as unique ID
      position: [latlng.lat, latlng.lng],
      name: `Marker ${markers.length + 1}`,
      description: 'Click to edit description',
      lat: latlng.lat,
      lng: latlng.lng
    }
    setMarkers([...markers, newMarker])
    setIsPlacingMarker(false) // Turn off placing mode after placing
  }

  const handleMarkerDelete = (id) => {
    setMarkers(markers.filter(marker => marker.id !== id))
  }

  const handleMarkerNameChange = (id, newName) => {
    setMarkers(markers.map(marker =>
      marker.id === id ? { ...marker, name: newName } : marker
    ))
  }

  const handleMarkerDescriptionChange = (id, newDescription) => {
    setMarkers(markers.map(marker =>
      marker.id === id ? { ...marker, description: newDescription } : marker
    ))
  }

  const togglePlacingMode = () => {
    setIsPlacingMarker(!isPlacingMarker)
  }

  const clearAllMarkers = () => {
    if (window.confirm('Are you sure you want to remove all markers?')) {
      setMarkers([])
    }
  }

  return (
    <div className="map-container">
      <SidePanel />

      {notification && (
        <div className={`notification ${notification.type}`}>
          {notification.message}
        </div>
      )}

      <div className="controls">
        <button
          className={`place-button ${isPlacingMarker ? 'active' : ''}`}
          onClick={togglePlacingMode}
        >
          {isPlacingMarker ? 'Cancel' : 'Place Pin'}
        </button>
        {markers.length > 0 && (
          <button className="clear-button" onClick={clearAllMarkers}>
            Clear All
          </button>
        )}
        {isPlacingMarker && (
          <div className="instruction">
            Tap the map to place your pin
          </div>
        )}
      </div>

      <MapContainer
        center={[48.8566, 2.3522]} // Paris coords
        zoom={13}
        scrollWheelZoom={true}
        style={{ height: '100%', width: '100%' }}
        ref={mapRef}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        <MapClickHandler onMapClick={handleMapClick} isPlacingMarker={isPlacingMarker} />

        {markers.map(marker => (
          <Marker
            key={marker.id}
            position={marker.position}
            icon={createCustomIcon('red')}
            eventHandlers={{
              click: () => {
                setActiveMarker(marker.id)
              }
            }}
          >
            <Popup onClose={() => setActiveMarker(null)}>
              <div className="marker-popup">
                <input
                  type="text"
                  value={marker.name}
                  onChange={(e) => handleMarkerNameChange(marker.id, e.target.value)}
                  placeholder="Pin name"
                  className="marker-name-input"
                />
                <textarea
                  value={marker.description}
                  onChange={(e) => handleMarkerDescriptionChange(marker.id, e.target.value)}
                  placeholder="Description"
                  className="marker-description-input"
                />
                <div className="popup-buttons">
                  <button
                    className={`save-marker-button ${savingMarkers[marker.id] ? 'saving' : ''}`}
                    disabled={savingMarkers[marker.id]}
                    onClick={async () => {
                      try {
                        // Set saving state for this marker
                        setSavingMarkers(prev => ({...prev, [marker.id]: true}));

                        // Prepare payload
                        const payload = {
                          title: marker.name,
                          description: marker.description,
                          lat: marker.lat || marker.position[0],
                          lng: marker.lng || marker.position[1]
                        };

                        // Call the API endpoint
                        const response = await fetch('http://localhost:8000/pins', {
                          method: 'POST',
                          headers: {
                            'Content-Type': 'application/json',
                          },
                          body: JSON.stringify(payload),
                        });

                        if (response.ok) {
                          // Remove the pin after successful save
                          handleMarkerDelete(marker.id);

                          // Show success notification instead of alert
                          showNotification('Pin saved successfully!', 'success');
                        } else {
                          throw new Error('Failed to save pin');
                        }
                      } catch (error) {
                        console.error('Error saving pin:', error);
                        showNotification('Failed to save pin. Please try again.', 'error');
                      } finally {
                        // Clear saving state
                        setSavingMarkers(prev => {
                          const newState = {...prev};
                          delete newState[marker.id];
                          return newState;
                        });
                      }
                    }}
                  >
                    {savingMarkers[marker.id] ? 'Saving...' : 'Save'}
                  </button>
                  <button
                    className="delete-marker-button"
                    onClick={() => handleMarkerDelete(marker.id)}
                  >
                    Delete
                  </button>
                </div>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  )
}
