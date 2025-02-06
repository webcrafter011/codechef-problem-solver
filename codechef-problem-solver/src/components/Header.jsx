import React from "react";

const Header = () => {
  return (
    <header className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-6 shadow-lg">
      <div className="container mx-auto text-center">
        <h1 className="text-4xl font-bold">CodeChef Solver</h1>
        <p className="mt-2 text-lg">
          AI-powered solutions for CodeChef problems
        </p>
      </div>
    </header>
  );
};

export default Header;
