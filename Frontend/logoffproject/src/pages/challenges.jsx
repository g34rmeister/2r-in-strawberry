import Card from "../components/card";

const Challenges = ({imgUrl,title,text}) => {
    imgUrl = !imgUrl ? "https://scontent-dfw5-2.xx.fbcdn.net/v/t39.30808-6/476148433_1167612378274157_7142023286726290425_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=833d8c&_nc_ohc=Obsy9c9Xd7cQ7kNvwEX2H4a&_nc_oc=Adm67Qd9u95Ncyqny24wkL9bOs-y-41z6CiED6j7JdwgWzdIR3QEqSqpbWcDLU-UtIBjnpyJNVWx5KOTJUdJ4y73&_nc_zt=23&_nc_ht=scontent-dfw5-2.xx&_nc_gid=tHgObA4Dgj61ge3Cq5UlQQ&oh=00_AfizVNfwafVE8j5_OFtbQXZwP1-tCfCIbfRL8AR0sdZD_w&oe=6915BBE9": imgUrl;
    title = !title ? "Quercus virginiana:" : title;
    text = !text ? "Evergreen oak tree native to the Southeastern United States, known for its long life and strong wood." : text;

    return (
        <div className="container">
            <Card imgUrl={imgUrl} title={title} text={text}></Card>
        </div>
    )
}

export default Challenges;
