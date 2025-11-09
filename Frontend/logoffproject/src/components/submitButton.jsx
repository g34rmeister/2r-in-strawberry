const SubmitButton = () => {
    return (
        <div className="button-section">
            <button type="button"
                    className="btn btn-primary submit-sample">
                <p className="button-text">
                    Submit Sample
                </p>
            </button>

            <button type="button"
                    className="btn btn-primary cancel-challenge">
                <p className="button-text">
                    Cancel Challenge
                </p>
            </button>
        </div>
    )
}

export default SubmitButton;