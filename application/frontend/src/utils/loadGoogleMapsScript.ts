export const loadGoogleMapsScript = (apiKey: string, callbackName: string) => {
  if (
    !document.querySelector(
      `script[src^="https://maps.googleapis.com/maps/api/js"]`
    )
  ) {
    const script = document.createElement("script");
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&callback=${callbackName}`;
    script.async = true;
    script.defer = true;
    script.onerror = (error) => {
      // Handle any errors that occur during the loading of the script
      console.error("Google Maps script failed to load.", error);
    };
    document.head.appendChild(script);
  }
};
