"use client";

import { HStack, Link, Stack, Text } from "@chakra-ui/react";

const links = [
  { label: "Security", href: "/security" },
  { label: "Status", href: "/status" },
  { label: "Docs", href: "/docs" },
  { label: "Privacy", href: "/legal/privacy" }
];

export function Footer() {
  return (
    <Stack as="footer" spacing={4} py={16} borderTop="1px solid" borderColor="whiteAlpha.200">
      <HStack spacing={6} justify={{ base: "flex-start", md: "center" }} flexWrap="wrap">
        {links.map((link) => (
          <Link
            key={link.label}
            href={link.href}
            color="whiteAlpha.600"
            _hover={{ color: "whiteAlpha.900" }}
            fontWeight="medium"
          >
            {link.label}
          </Link>
        ))}
      </HStack>
      <Text textAlign={{ base: "left", md: "center" }} color="whiteAlpha.500" fontSize="sm">
        © {new Date().getFullYear()} Agent Orchestration Platform. All rights reserved.
      </Text>
    </Stack>
  );
}
