// src/components/Footer.js
import React from "react";
import styled from "styled-components";

const FooterWrapper = styled.footer`
  background-color: #111;
  color: #fff;
  padding: 0.1rem; /* Reduced padding to make the footer shorter */
  text-align: center;
  font-size: 0.475rem;
`;

function Footer() {
  return (
    <FooterWrapper>
      <p>&copy; 2024 Rise UP. All rights reserved.</p>
    </FooterWrapper>
  );
}

export default Footer;
