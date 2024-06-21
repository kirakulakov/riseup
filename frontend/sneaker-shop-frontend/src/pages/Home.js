// src/pages/Home.js
import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { Link, useNavigate } from "react-router-dom";

const HomeWrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
`;

const Title = styled.h1`
  font-size: 3rem;
  margin-bottom: 1rem;
  text-align: center; /* Center the text */
`;

const Subtitle = styled.p`
  font-size: 1.5rem;
  margin-bottom: 2rem;
  text-align: center; /* Center the text */
`;

const CTAButton = styled(Link)`
  background-color: #111;
  color: #fff;
  padding: 1rem 2rem;
  text-decoration: none;
  font-size: 1.2rem;
  border-radius: 4px;
  transition: background-color 0.3s;

  &:hover {
    background-color: #333;
  }
`;

const NavBar = styled.nav`
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 2rem;
  background-color: #f8f8f8;
  padding: 1rem;
  width: 100%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);

  @media (max-width: 768px) {
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }
`;

const NavLink = styled(Link)`
  color: #111;
  text-decoration: none;
  font-size: 1.2rem;
  font-weight: bold;

  &:hover {
    text-decoration: underline;
  }

  @media (max-width: 768px) {
    font-size: 1rem;
  }
`;

const SignOutButton = styled.button`
  background: none;
  border: none;
  color: #111;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  &:hover {
    text-decoration: underline;
  }
  @media (max-width: 768px) {
    font-size: 1rem;
  }
`;

function Home() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    setIsAuthenticated(!!token);
  }, []);

  const handleSignOut = () => {
    localStorage.removeItem("token");
    setIsAuthenticated(false);
    // Optionally, you can redirect to the home page or login page
    // navigate("/");
  };

  return (
    <HomeWrapper>
      <NavBar>
        <NavLink to="/new-featured">New & Featured</NavLink>
        <NavLink to="/men">Men</NavLink>
        <NavLink to="/women">Women</NavLink>
        <NavLink to="/kids">Kids</NavLink>
        <NavLink to="/jordan">Jordan</NavLink>
        {isAuthenticated ? (
          <SignOutButton onClick={handleSignOut}>Sign Out</SignOutButton>
        ) : (
          <NavLink to="/auth">Sign In</NavLink>
        )}
      </NavBar>
      <Title>Добро пожаловать в Rise Up Shop</Title>
      <Subtitle>Лучшие кроссовки по доступным ценам</Subtitle>
      <CTAButton to="/products">Shop Now</CTAButton>
    </HomeWrapper>
  );
}
export default Home;
