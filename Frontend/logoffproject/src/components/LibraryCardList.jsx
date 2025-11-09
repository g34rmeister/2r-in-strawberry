// components/LibraryCardList.jsx

import Card from './card';

// Utility function to format the date
const formatDate = (dateString) => {
    if (!dateString) return 'Date N/A';
    // Use a more robust date field name like 'date_collected' if available
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
};

// Component to render the list of cards
const LibraryCardList = ({ libraryData }) => {
    if (!libraryData || libraryData.length === 0) {
        return <p className="empty-collection-message">Your collection is currently empty!</p>;
    }

    return (
        <div className="history-cards-wrapper">
            {libraryData.map((card, index) => (
                <div key={card.id || index} className="history-card-item">
                    <Card
                        // Map Django/JSON fields to Card Component Props
                        // NOTE: Ensure these fields match your actual Django serializer output!
                        imgUrl={card.image || card.imgUrl}
                        name={card.name}
                        text={card.description || card.text}
                        
                        // Instantiating/Mapping other fields
                        // Assuming location_found maps to the card's main title
                        title={card.location_found || "Unknown Location"} 
                        // Assuming rarity is sent, otherwise default
                        rarity={card.rarity || "Common"} 
                        // Setting quality to a fixed value as per your request
                        quality={"10"} 
                        
                        // Auto-instantiated Date (Assuming the backend uses 'date_collected')
                        dateCollected={formatDate(card.date_collected || card.created_at)} 
                    />
                </div>
            ))}
        </div>
    );
};

export default LibraryCardList;