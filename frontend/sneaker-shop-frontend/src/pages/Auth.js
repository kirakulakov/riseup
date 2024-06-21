// src/pages/Auth.js
import React, { useState, useEffect } from "react";
import styled from "styled-components";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { initTelegramAuth, getTelegramAuthData } from "../utils/telegram";

const AuthWrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
`;

const Title = styled.h2`
  font-size: 2rem;
  margin-bottom: 1rem;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 300px;
`;

const Input = styled.input`
  margin-bottom: 1rem;
  padding: 0.5rem;
  font-size: 1rem;
`;

const Button = styled.button`
  background-color: #111;
  color: #fff;
  padding: 0.5rem;
  font-size: 1rem;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;

  &:hover {
    background-color: #333;
  }
`;

function Auth() {
  const [telegramAuth, setTelegramAuth] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const initAuth = async () => {
      try {
        const webApp = await initTelegramAuth();
        setTelegramAuth(webApp);
      } catch (error) {
        console.error("Failed to initialize Telegram auth:", error);
      }
    };

    initAuth();
  }, []);

  const handleTelegramAuth = async () => {
    if (telegramAuth) {
      const authData = getTelegramAuthData(telegramAuth);
      if (authData) {
        try {
          const response = await axios.post(
            "http://localhost:8000/sign-in-or-up",
            // "https://fifty-jars-deny.loca.lt/sign-in-or-up",
            authData
          );
          localStorage.setItem("token", response.data.access_token);
          navigate("/");
        } catch (error) {
          console.error("Authentication error:", error);
        }
      } else {
        console.error("Telegram auth data not available");
      }
    }
  };

  return (
    <AuthWrapper>
      <Title>Sign In with Telegram</Title>
      <Button onClick={handleTelegramAuth} disabled={!telegramAuth}>
        {telegramAuth ? "Sign In with Telegram" : "Loading Telegram Auth..."}
      </Button>
    </AuthWrapper>
  );
}

export default Auth;
