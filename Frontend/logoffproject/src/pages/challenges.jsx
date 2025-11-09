import Card from "../components/card";
import api from "../components/api";
import { useEffect, useState } from "react";

const Challenges = ({imgUrl,title,text}) => {
    const [challenge, setChallenge] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchChallenge = async () => {
            try {
                const response = await api.get('/plantnet/getchallenge/');
                setChallenge(response.data);
            } catch(error) {
                console.error("Error fetching challenge", error);
            } finally {
                setIsLoading(false);
            };
        };
        fetchChallenge();
    }, [])

    if (!challenge || !challenge['scientific-name']) {
        return (
            <div className="container">
                <h2>No Active Challenge</h2>
                <p>Visit the "Get Plant" page to start a new challenge!</p>
            </div>
        );
    }

    return (
        <div className="container">
            <Card
             imgUrl={challenge['image-url']} 
             name = {challenge['common-name']}
             rarity = "★★"
             title={challenge['scientific-name']}
             text={challenge['description']}
             />
        </div>
    )
}
export default Challenges;
