import React from 'react';

interface ImageDisplayProps {
  imageBase64: string;
}

const ImageDisplay: React.FC<ImageDisplayProps> = ({ imageBase64 }) => {
  if (!imageBase64) return null;

  return (
    <div className="mt-4">
      <p className="font-medium">Generated Visualization:</p>
      <img
        src={`data:image/png;base64,${imageBase64}`}
        alt="Generated visualization"
        className="mt-2 max-w-full h-auto rounded shadow-lg"
      />
    </div>
  );
};

export default ImageDisplay; 