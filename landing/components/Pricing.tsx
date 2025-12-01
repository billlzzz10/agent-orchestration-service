"use client";

import {
  Badge,
  Box,
  Button,
  Flex,
  Grid,
  Heading,
  HStack,
  Icon,
  List,
  ListIcon,
  ListItem,
  Stack,
  Text,
  useColorModeValue
} from "@chakra-ui/react";
import { FiCheck, FiShield, FiUsers } from "react-icons/fi";

const tiers = [
  {
    name: "Starter",
    price: "$49",
    description: "Launch your first orchestrated agent workflows with built-in security defaults.",
    cta: "Start free trial",
    href: "/signup",
    features: [
      "Up to 5 concurrent workflows",
      "Role-based access controls",
      "Audit-ready event streams",
      "Community support"
    ],
    icon: FiUsers
  },
  {
    name: "Growth",
    price: "$249",
    description: "Scale mission-critical automations with staging environments and analytics dashboards.",
    cta: "Contact sales",
    href: "/contact",
    features: [
      "Unlimited orchestrations",
      "Advanced guardrails",
      "SLO dashboards & alerting",
      "Single Sign-On"
    ],
    icon: FiShield,
    highlighted: true
  },
  {
    name: "Enterprise",
    price: "Custom",
    description: "Meet the strictest compliance standards with private networking and on-prem options.",
    cta: "Book strategy session",
    href: "/enterprise",
    features: [
      "Dedicated compliance concierge",
      "Isolated control plane",
      "Custom data residency",
      "24/7 premium support"
    ],
    icon: FiCheck
  }
];

export function Pricing() {
  const cardBg = useColorModeValue("whiteAlpha.200", "whiteAlpha.100");
  const border = useColorModeValue("whiteAlpha.300", "whiteAlpha.200");

  return (
    <Stack as="section" spacing={12} py={{ base: 16, lg: 24 }}>
      <Stack spacing={4} textAlign="center" maxW="3xl" mx="auto">
        <Heading size="2xl">Pricing that scales with your governance needs</Heading>
        <Text fontSize="lg" color="whiteAlpha.700">
          Start with proven defaults and upgrade when your automation programs expand. Every
          plan includes proactive security features.
        </Text>
      </Stack>
      <Grid
        templateColumns={{ base: "1fr", md: "repeat(3, minmax(0, 1fr))" }}
        gap={{ base: 8, lg: 10 }}
      >
        {tiers.map((tier) => (
          <Box
            key={tier.name}
            p={{ base: 8, md: 10 }}
            borderRadius="2xl"
            bg={cardBg}
            border="1px solid"
            borderColor={border}
            backdropFilter="auto"
            backdropBlur="28px"
            position="relative"
            boxShadow={tier.highlighted ? "0 20px 60px rgba(30, 64, 175, 0.55)" : undefined}
            transform={tier.highlighted ? "scale(1.02)" : undefined}
            transition="transform 0.3s ease"
            _hover={{ transform: tier.highlighted ? "scale(1.04)" : "translateY(-4px)" }}
          >
            {tier.highlighted ? (
              <Badge
                position="absolute"
                top={4}
                right={4}
                colorScheme="brand"
                variant="solid"
              >
                Most popular
              </Badge>
            ) : null}
            <Stack spacing={6}>
              <HStack spacing={3} align="center">
                <Flex
                  w={12}
                  h={12}
                  borderRadius="full"
                  align="center"
                  justify="center"
                  bg="brand.500"
                  color="white"
                >
                  <Icon as={tier.icon} boxSize={6} />
                </Flex>
                <Heading size="lg">{tier.name}</Heading>
              </HStack>
              <Stack spacing={1}>
                <Text fontSize="4xl" fontWeight="bold">
                  {tier.price}
                </Text>
                <Text color="whiteAlpha.700">{tier.description}</Text>
              </Stack>
              <List spacing={3} color="whiteAlpha.800">
                {tier.features.map((feature) => (
                  <ListItem key={feature}>
                    <ListIcon as={FiCheck} color="brand.400" />
                    {feature}
                  </ListItem>
                ))}
              </List>
              <Button
                as="a"
                href={tier.href}
                size="lg"
                colorScheme={tier.highlighted ? "brand" : undefined}
                variant={tier.highlighted ? "solid" : "outline"}
                borderColor={tier.highlighted ? undefined : "whiteAlpha.400"}
                _hover={
                  tier.highlighted
                    ? undefined
                    : { borderColor: "whiteAlpha.700", bg: "whiteAlpha.200" }
                }
              >
                {tier.cta}
              </Button>
            </Stack>
          </Box>
        ))}
      </Grid>
    </Stack>
  );
}
