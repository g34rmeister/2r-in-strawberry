import Card from '../components/card';
import Navbar from '../components/navbar';

const cards = [
    {
        imgUrl: "https://images.unsplash.com/photo-1441974231531-c6227db76b6e",
        name: "Southern Live Oak",
        rarity: "★★",
        quality: "10",
        dateCollected: "11-9-2025",
        title: "Majestic Oak",
        text: "Found in the park"
    },
    {
        imgUrl: "https://images.unsplash.com/photo-1502082553048-f009c37129b9",
        name: "Maple Tree",
        rarity: "★",
        quality: "8",
        dateCollected: "11-8-2025",
        title: "Red Maple",
        text: "Beautiful fall colors"
    },
    {
        imgUrl: "https://images.unsplash.com/photo-1513836279014-a89f7a76ae86",
        name: "Pine Tree",
        rarity: "★★★",
        quality: "9",
        dateCollected: "11-7-2025",
        title: "Ancient Pine",
        text: "Rare specimen"
    }
];

function History() {
    return (
        <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
            <h2 style={{ padding: '20px', margin: 0 }}>Your Collection</h2>
            <div style={{ 
                flex: 1,
                overflowY: 'auto',
                padding: '0 20px 20px 20px'
            }}>
                {cards.map((card, index) => (
                    <div key={index} style={{ marginBottom: '15px' }}>
                        <Card
                            imgUrl={card.imgUrl}
                            name={card.name}
                            rarity={card.rarity}
                            quality={card.quality}
                            title={card.title}
                            text={card.text}
                            dateCollected={card.dateCollected}
                        />
                    </div>
                ))}
            </div>
            <Navbar />
        </div>
    );
}

export default History;