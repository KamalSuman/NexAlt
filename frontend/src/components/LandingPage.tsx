import React, { useState } from "react";
import LoginImgVector from "@/assets/login-im.svg";
import BG2 from "@/assets/bg2.svg";
import BG4 from "@/assets/bg4.svg";
import Logo from "@/assets/logo.svg";
import { Link } from "react-router-dom";

export default function LandingPage() {
  const [showLogin, setShowLogin] = useState(false);

  const toggleLogin = () => setShowLogin(!showLogin);

  return (
    <div className="relative bg-gray-50 text-gray-800 overflow-hidden">
      {/* Decorative Background Images */}
      <img
        src={BG4}
        alt="Background 1"
        className="absolute top-5 left-0 opacity-70 z-[1] pointer-events-none w-1/5"
      />
      <img
        src={BG2}
        alt="Background 2"
        className="absolute top-40 right-0 w-1/4 opacity-70 z-[1] pointer-events-none"
      />
      {/* Header */}
      <header className="bg-white shadow p-3 pb-4 flex justify-between items-center">
        <h1 className="text-3xl font-bold text-black cursor-pointer">
          nexAlt.ai
        </h1>
        {/* <img src={Logo} alt="Logo" className="h-6" /> */}
        <nav>
          <ul className="flex gap-6 text-sm font-medium items-center">
            <li>
              <a href="#features" className="hover:text-blue-600">
                Features
              </a>
            </li>
            <li>
              <a href="#about" className="hover:text-blue-600">
                About
              </a>
            </li>
            <li>
              <a href="#contact" className="hover:text-blue-600">
                Contact
              </a>
            </li>
            <li>
              <button
                onClick={toggleLogin}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
              >
                Login
              </button>
            </li>
          </ul>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="text-center py-20 px-4 bg-gradient-to-r from-blue-100 to-purple-100">
        <h2 className="text-4xl font-bold mb-4">
          Next-Gen Portfolio Management Tool
        </h2>
        <p className="max-w-xl mx-auto text-lg text-gray-700">
          Build intelligent, personalized, and optimal portfolios using investor
          profiling, Monte Carlo simulations, and AI-driven deep learning.
        </p>
        <Link
          to={"/chatbot/"}
          className="mt-6 inline-block px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition"
        >
          Get Started
        </Link>
      </section>

      {/* Features Section */}
      <section id="features" className="py-16 px-6 bg-white">
        <div className="text-center mb-12">
          <h3 className="text-3xl font-semibold">Key Features</h3>
          <p className="text-gray-600 mt-2">
            Smart, scalable, and fully customizable
          </p>
        </div>
        <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-10 text-center">
          <div className="p-6 bg-gray-100 rounded-lg shadow">
            <h4 className="font-bold text-lg mb-2">Investor Profiling</h4>
            <p>
              Understand user goals, risk preferences, and financial backgrounds
              using AI-driven surveys and analytics.
            </p>
          </div>
          <div className="p-6 bg-gray-100 rounded-lg shadow">
            <h4 className="font-bold text-lg mb-2">Asset Class Modeling</h4>
            <p>
              Use data-driven insights to model equity, debt, gold, and
              alternative assets with correlation awareness.
            </p>
          </div>
          <div className="p-6 bg-gray-100 rounded-lg shadow">
            <h4 className="font-bold text-lg mb-2">
              Deep Learning Personalization
            </h4>
            <p>
              Leverage neural networks to optimize and adjust portfolios over
              time for each unique investor journey.
            </p>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-16 px-6 bg-gray-50 text-center">
        <div className="max-w-3xl mx-auto">
          <h3 className="text-2xl font-bold mb-4">About the Project</h3>
          <p className="text-gray-700">
            This platform merges traditional finance principles with modern AI
            technologies to bring real-world, customizable portfolio solutions
            to individuals and advisors alike. Built with Monte Carlo
            simulation, rule-based screening, and deep learning, our system is
            designed for transparency, adaptability, and performance.
          </p>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-16 px-6 bg-white text-center">
        <h3 className="text-2xl font-bold mb-4">Get in Touch</h3>
        <p className="text-gray-600 mb-6">
          Interested in our intelligent portfolio system? Let’s talk.
        </p>
        <a
          href="mailto:info@smartportfolio.ai"
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Contact Us
        </a>
      </section>

      {/* Login Modal */}
      {showLogin && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
          <div className="bg-white rounded-lg overflow-hidden w-full max-w-4xl flex">
            <div className="w-1/2 bg-white hidden md:flex items-center justify-center p-6">
              <img
                src={LoginImgVector}
                alt="Login Illustration"
                className="scale-125 ml-3"
              />
            </div>
            <div className="w-full md:w-1/2 p-8">
              <h2 className="text-3xl font-bold mb-2 text-gray-800">
                Welcome to NextAlt.ai! 👋🏻
              </h2>
              <p className="mb-6 text-gray-500">
                Please sign in to your account and start the adventure
              </p>
              <form>
                <div className="mb-4">
                  <label className="block mb-1 text-sm text-gray-600">
                    Email
                  </label>
                  <input
                    type="email"
                    className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Enter your email"
                  />
                </div>
                <div className="mb-4">
                  <label className="block mb-1 text-sm text-gray-600">
                    Password
                  </label>
                  <input
                    type="password"
                    className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Enter your password"
                  />
                  <div className="text-right mt-1">
                    <a
                      href="#"
                      className="text-sm text-blue-500 hover:underline"
                    >
                      Forgot Password?
                    </a>
                  </div>
                </div>
                <div className="mb-4 flex items-center">
                  <input type="checkbox" id="remember" className="mr-2" />
                  <label htmlFor="remember" className="text-sm text-gray-600">
                    Remember Me
                  </label>
                </div>
                <Link to={"/chatbot/"}>
                  <button
                    type="submit"
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg"
                  >
                    Sign In
                  </button>
                </Link>
              </form>
              <p className="mt-6 text-center text-sm text-gray-600">
                New on our platform?{" "}
                <a href="#" className="text-blue-500 hover:underline">
                  Create an account
                </a>
              </p>
              <div className="mt-6 flex justify-center space-x-4 text-lg">
                <a href="#" className="text-blue-700 hover:text-blue-900">
                  <i className="fab fa-facebook-f"></i>
                </a>
                <a href="#" className="text-blue-400 hover:text-blue-600">
                  <i className="fab fa-twitter"></i>
                </a>
                <a href="#" className="text-black hover:text-gray-700">
                  <i className="fab fa-github"></i>
                </a>
                <a href="#" className="text-red-600 hover:text-red-800">
                  <i className="fab fa-google"></i>
                </a>
              </div>
              <button
                onClick={toggleLogin}
                className="mt-4 text-sm text-gray-500 hover:underline block mx-auto"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="bg-gray-100 py-6 text-center text-sm text-gray-500">
        &copy; 2025 SmartPortfolio.ai | All rights reserved.
      </footer>
    </div>
  );
}
