const ImageBox = ({imgUrl}) => {
    return (
        <div className="image-box">
            <img src={`http://localhost:8000${imgUrl}`}
            alt="Live Oak Tree picture" />
        </div>
    )
}

export default ImageBox;