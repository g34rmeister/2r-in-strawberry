import ImageBox from "./imageBox";
import PlantDescription from "./plantDescription";
import PlanTitle from "./plantTitle";

const Card = ({imgUrl,title,text}) => {
    return(
            <div className="card-container">
                <div className="card-image">
                    <ImageBox imgUrl={imgUrl}></ImageBox>
                </div>
                <div className="title-description-container">
                    <PlanTitle title={title}></PlanTitle>
                    <PlantDescription text={text}></PlantDescription>
                </div>
            </div>
        )
};

export default Card;