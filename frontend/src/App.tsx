import React from 'react';
import Chat from './components/Chat';

const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-4xl mx-auto py-6 px-4">
          <h1 className="text-3xl font-bold text-gray-900">
            Visualization Generator
          </h1>
        </div>
      </header>
      <main>
        <Chat />
      </main>
    </div>
  );
};

export default App; 