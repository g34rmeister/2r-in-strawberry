// History.jsx

import Navbar from '../components/navbar';
import api from '../components/api';
import LibraryCardList from '../components/LibraryCardList'; // Import the new component
import { useState, useEffect } from 'react';

function History() {
    const [libraryData, setLibraryData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchLibrary = async () => {
            try {
                const response = await api.get('userdata/library/');
                setLibraryData(response.data);
                setError(null);
            } catch (err) {
                console.error("Error fetching library:", err.response ? err.response.data : err.message);
                
                let errorMessage = "Failed to load collection data. Please try again.";
                if (err.response && err.response.status === 401) {
                    errorMessage = "Authentication required. Please log in.";
                }
                setError(errorMessage);
            } finally {
                setLoading(false);
            }
        };
        fetchLibrary();
    }, []);

    // --- Loading State ---
    if (loading) {
        return (
            <div className="history-container">
                <h2 className="history-header">Loading your collection...</h2>
                <Navbar />
            </div>
        );
    }

    // --- Error State ---
    if (error) {
        return (
            <div className="history-container">
                <h2 className="history-header">Your Collection</h2>
                <p className="error-message">{error}</p>
                <Navbar />
            </div>
        );
    }

    // --- Success State (Main Content) ---
    return (
        <div className="history-container">
            <h2 className="history-header">Your Collection</h2>
            {/* Render the card list component, passing the data */}
            <LibraryCardList libraryData={libraryData} />
            <Navbar />
        </div>
    );
}

export default History;