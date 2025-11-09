import Card from "../components/card";
import api from "../components/api";
// 1. Combined React imports into one line
import React, { useEffect, useState, useRef } from "react";

const difficultyStars = {
    1: '★',
    2: '★★',
    3: '★★★'
};

const submit_url = "userdata/add-to-library";

// 2. Removed unused props (imgUrl, title, text)
const Challenges = () => {
    const [challenge, setChallenge] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    const [isSubmitting, setIsSubmitting] = useState(false);
    const [submitError, setSubmitError] = useState(null);

    const fileInputRef = useRef(null);

    useEffect(() => {
        const fetchChallenge = async () => {
            setIsLoading(true); // Set loading to true when starting fetch
            try {
                const response = await api.get('/plantnet/getchallenge/');
                setChallenge(response.data);
            } catch (error) {
                console.error("Error fetching challenge", error);
            } finally {
                setIsLoading(false);
            };
        };
        fetchChallenge();
    }, []);

    const handleFileSubmit = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        if (!challenge || !challenge['scientific-name']) {
            setSubmitError("Challenge is not loaded. Please refresh.");
            return;
        }

        setIsSubmitting(true);
        setSubmitError(null);

        const formData = new FormData();
        formData.append('image', file);
        formData.append('correct-species', challenge['scientific-name']);

        try {
            const response = await api.post('plantnet/validateplant/', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });

            if (response.data.correct === true) {
                await addToLibrary(challenge);
                alert("Correct! Plant added to your library.");
            } else {
                setSubmitError("That's not the right plant. Try again!");
            }
        } catch (err) {
            console.error("Error during submission:", err);
            setSubmitError("An error occurred. Please try again.");
        } finally {
            setIsSubmitting(false);
            event.target.value = null;
        }
    };

    const addToLibrary = async (plantData) => {
        console.log("Calling next API:", submit_url);
        console.log("Adding plant to library:", plantData['scientific-name']);
        // Your next API call logic goes here
    };

    // 3. Added a check for the isLoading state
    if (isLoading) {
        return (
            <div className="container">
                <h2>Loading Challenge...</h2>
            </div>
        );
    }

    if (!challenge || !challenge['scientific-name']) {
        return (
            <div className="container">
                <h2>No Active Challenge</h2>
                <p>Visit the "Get Plant" page to start a new challenge!</p>
            </div>
        );
    }

    const starRating = difficultyStars[challenge['dificulty']] || 'N/A';

    return (
        <div className="container">
            <Card
                imgUrl={challenge['image-url']}
                name={challenge['common-name']}
                rarity={starRating}
                title={challenge['scientific-name']}
                text={challenge['description']}
            />

            <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileSubmit}
                style={{ display: 'none' }}
                accept="image/*"
            />

            <div className="button-section">
                <button
                    type="button"
                    className="btn btn-primary submit-sample"
                    onClick={() => fileInputRef.current.click()}
                    disabled={isSubmitting}
                >
                    <p className="button-text">
                        {isSubmitting ? "Submitting..." : "Submit Sample"}
                    </p>
                </button>
                <button type="button"
                    className="btn btn-primary cancel-challenge">
                    <p className="button-text">
                        Cancel Challenge
                    </p>
                </button>
            </div>

            {/* 4. Added a place to show the submission error */}
            {submitError && <p style={{ color: 'red', marginTop: '10px' }}>{submitError}</p>}
        </div>
    );
}

export default Challenges;