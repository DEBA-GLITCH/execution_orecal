import React from 'react';
import { Zap, Plus } from 'lucide-react';

export default function TopBar() {
  return (
    <nav className="fixed top-0 right-0 left-64 z-50 glass border-b border-white/10">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex items-center justify-between h-16">
          {/* Logo Section */}
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
              <Zap size={18} fill="white" className="text-white" />
            </div>
            <span className="font-bold text-xl tracking-tight">
              Exec<span className="gradient-text">AI</span>
            </span>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center gap-4">
            <button className="hidden sm:flex items-center gap-2 px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 transition-all text-sm font-semibold shadow-md shadow-blue-600/20">
              <Plus size={16} strokeWidth={3} />
              New Project
            </button>
            
            <div className="h-8 w-[1px] bg-white/10 mx-2"></div>
            
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-xs font-bold border border-white/20">
              JD
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}