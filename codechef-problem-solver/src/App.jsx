import React from "react";
import Header from "./components/Header";
import ProblemSolver from "./components/ProblemSolver";

const App = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <ProblemSolver />
    </div>
  );
};

export default App;
