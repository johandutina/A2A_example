import React from 'react';

interface CodeDisplayProps {
  code: string;
}

const CodeDisplay: React.FC<CodeDisplayProps> = ({ code }) => {
  return (
    <div className="mt-2">
      <p className="font-medium">Generated Code:</p>
      <pre className="bg-gray-800 text-white p-2 rounded mt-1 overflow-x-auto">
        {code}
      </pre>
    </div>
  );
};

export default CodeDisplay; 