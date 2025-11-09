const ImageBox = ({imgUrl}) => {
    return (
        <div className="image-box">
            <img src={imgUrl}
            alt="Live Oak Tree picture" />
        </div>
    )
}

export default ImageBox;