// src/components/Header.js
import React from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";

const HeaderWrapper = styled.header`
  background-color: #111;
  padding: 1rem;
`;

const Nav = styled.nav`
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const Logo = styled(Link)`
  color: #fff;
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
`;

const NavLinks = styled.div`
  display: flex;
  gap: 1rem;
`;

const NavLink = styled(Link)`
  color: #fff;
  text-decoration: none;
  margin-right: 20px;

  &:hover {
    text-decoration: underline;
  }
`;

function Header() {
  return (
    <HeaderWrapper>
      <Nav>
        <Logo to="/">RISE</Logo>
        <NavLinks>
          {/* <NavLink to="/products">Каталог</NavLink> */}
          <NavLink to="/auth">Вход</NavLink>
        </NavLinks>
      </Nav>
    </HeaderWrapper>
  );
}

export default Header;
