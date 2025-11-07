"use client";

import {
  Avatar,
  Box,
  Grid,
  Heading,
  Stack,
  Text,
  useColorModeValue
} from "@chakra-ui/react";

const testimonials = [
  {
    name: "Riya Desai",
    role: "VP of Automation, LatticeWorks",
    quote:
      "We reduced governance review cycles from weeks to hours. The pre-built controls made our security team instant fans.",
    avatar: "https://avatars.githubusercontent.com/u/9942277?v=4"
  },
  {
    name: "Oliver Martinez",
    role: "Head of AI, Nova Logistics",
    quote:
      "Telemetry from day one meant we could iterate confidently. The Saas UI components let us ship a polished experience fast.",
    avatar: "https://avatars.githubusercontent.com/u/16960284?v=4"
  },
  {
    name: "Anika Johansson",
    role: "Product Lead, Aurora Analytics",
    quote:
      "Their orchestration runtime let us orchestrate 20+ agents without rewriting our tooling. We hit SOC2 milestones on schedule.",
    avatar: "https://avatars.githubusercontent.com/u/3722367?v=4"
  }
];

export function Testimonials() {
  const cardBg = useColorModeValue("whiteAlpha.200", "whiteAlpha.100");
  const border = useColorModeValue("whiteAlpha.300", "whiteAlpha.200");

  return (
    <Stack as="section" spacing={12} py={{ base: 16, lg: 24 }}>
      <Stack spacing={4} textAlign="center">
        <Heading size="2xl">Trusted by teams shipping AI responsibly</Heading>
        <Text fontSize="lg" color="whiteAlpha.700" maxW="3xl" mx="auto">
          Security, observability, and usability don&apos;t have to be trade-offs. Hear from
          leaders who orchestrate production AI with confidence.
        </Text>
      </Stack>
      <Grid templateColumns={{ base: "1fr", md: "repeat(3, 1fr)" }} gap={{ base: 8, lg: 10 }}>
        {testimonials.map((testimonial) => (
          <Box
            key={testimonial.name}
            p={8}
            borderRadius="2xl"
            bg={cardBg}
            border="1px solid"
            borderColor={border}
            backdropFilter="auto"
            backdropBlur="24px"
          >
            <Text fontSize="lg" color="whiteAlpha.800" mb={8}>
              “{testimonial.quote}”
            </Text>
            <Stack direction="row" align="center" spacing={4}>
              <Avatar name={testimonial.name} src={testimonial.avatar} />
              <Stack spacing={0}>
                <Text fontWeight="semibold">{testimonial.name}</Text>
                <Text fontSize="sm" color="whiteAlpha.600">
                  {testimonial.role}
                </Text>
              </Stack>
            </Stack>
          </Box>
        ))}
      </Grid>
    </Stack>
  );
}
