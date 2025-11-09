import ImageBox from "./imageBox";
import PlantDescription from "./plantDescription";
import PlanTitle from "./plantTitle";

const Card = ({
    imgUrl,
    name,
    rarity,
    quality,
    title,
    text,
    dateCollected
}) => {
    return(
        <div className="card-container">
            <div className="card-grid">

                <div className="card-name">
                    <h2>{name}</h2>
                </div>

                <div className="card-image">
                    <ImageBox imgUrl={imgUrl} />
                </div>
                <div className = "info-container">
                    <div className="card-title">
                        <PlanTitle title={title} />
                    </div>

                    <div className="card-description">
                        <PlantDescription text={text} />
                    </div>
                    <div className="card-stats">
                        <p><strong>Rarity:</strong> {rarity}</p>
                        <p><strong>Quality:</strong> {quality}</p>
                    </div>
                    <div className="card-date">
                        Collected: {dateCollected}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Card;