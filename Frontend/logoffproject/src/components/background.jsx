function BackgroundImage({backgroundImageUrl}) {
  return (
    <div style={{
      position: 'relative',
      minHeight: '100vh'
    }}>
      {/* Background image layer */}
      {/* Background layer */}
        <div style={{
        position: 'fixed',  // Changed to fixed
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundImage: 'url("https://images.unsplash.com/photo-1533038590840-1cde6e668a91?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=687")',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        opacity: 0.3,
        zIndex: -1
        }} />
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundImage: `url("${backgroundImageUrl}")`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        opacity: 0.3,  // Adjust transparency (0-1)
        zIndex: -1
      }} />
    </div>
  );
}

export default BackgroundImage;