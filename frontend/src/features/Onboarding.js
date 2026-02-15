import React, { useState } from 'react';

export const Onboarding = ({ onPlanGenerated }) => {
  const [idea, setIdea] = useState("");

  const handleGenerate = async () => {
    try {
      const res = await fetch("http://localhost:8000/start-project", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ idea })
      });
      const plan = await res.json();
      console.log("Received plan:", plan);
      onPlanGenerated(plan);
    } catch (error) {
      console.error("Error generating plan:", error);
      alert("Failed to generate plan: " + error.message);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4 text-center">
      <h1 className="text-5xl font-bold mb-6">Turn ideas into <span className="text-blue-400">Action</span></h1>
      <textarea 
        className="w-full max-w-2xl bg-white/5 border border-white/10 rounded-xl p-4 text-white"
        placeholder="Describe your project idea..."
        onChange={(e) => setIdea(e.target.value)}
      />
      <button 
        onClick={handleGenerate}
        disabled={!idea.trim()}
        className="mt-6 px-8 py-3 bg-blue-600 rounded-lg font-bold hover:bg-blue-500 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Generate Execution Plan
      </button>
    </div>
  );
};