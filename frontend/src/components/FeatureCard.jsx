import React from 'react';

export default function FeatureCard({ icon, title, desc }) {
  return (
    <div className="glass p-8 rounded-3xl text-center hover:bg-white/[0.06] transition-all duration-300 group cursor-default border border-white/[0.05] hover:border-white/20">
      <div className="w-14 h-14 rounded-2xl bg-white/5 flex items-center justify-center mx-auto mb-6 group-hover:scale-110 group-hover:bg-gradient-to-br group-hover:from-blue-500/20 group-hover:to-purple-500/20 transition-all duration-500">
        {React.cloneElement(icon, { size: 28, strokeWidth: 1.5 })}
      </div>
      <h3 className="text-lg font-bold mb-3 text-white group-hover:text-blue-300 transition-colors">
        {title}
      </h3>
      <p className="text-gray-400 text-sm leading-relaxed px-2">
        {desc}
      </p>
    </div>
  );
}