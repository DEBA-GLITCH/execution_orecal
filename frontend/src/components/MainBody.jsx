import React from 'react';

export default function MainBody({ children }) {
  return (
    <div className="flex-1 ml-64 min-h-screen bg-[#0f0f23]">
      {/* Background Glow Decorations */}
      <div className="fixed top-[-10%] left-[20%] w-[500px] h-[500px] bg-blue-600/10 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="fixed bottom-[10%] right-[5%] w-[400px] h-[400px] bg-purple-600/10 rounded-full blur-[100px] pointer-events-none"></div>
      
      <div className="relative z-10 pt-24 pb-16 px-8 max-w-6xl mx-auto">
        {children}
      </div>
    </div>
  );
}