// src/components/PopularSneakers.js
import React from "react";
import styled from "styled-components";

const RibbonWrapper = styled.div`
  width: 100%;
  overflow-x: auto;
  padding: 2rem 0;
`;

const RibbonTitle = styled.h2`
  font-size: 1.5rem;
  margin-bottom: 1rem;
  padding-left: 2rem;
`;

const RibbonContent = styled.div`
  display: flex;
  gap: 1rem;
  padding: 0 2rem;
`;

const SneakerCard = styled.div`
  flex: 0 0 auto;
  width: 300px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s ease;

  &:hover {
    transform: translateY(-5px);
  }
`;

const SneakerImage = styled.img`
  width: 100%;
  height: 200px;
  object-fit: cover;
`;

const SneakerInfo = styled.div`
  padding: 1rem;
`;

const SneakerName = styled.h3`
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
`;

const SneakerPrice = styled.p`
  font-size: 1rem;
  font-weight: bold;
`;

const sneakers = [
  {
    id: 1,
    name: "Nike Air Max 90",
    description:
      "The Air Jordan 1 Retro High is a classic sneaker that never goes out of style.",
    price: 9999,
    image_url:
      "https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/zwxes8uud05rkuei1mpt/air-max-90-mens-shoes-6n3vKB.png",
  },
  {
    id: 2,
    name: "Nike Air Force 1 LV8 5",
    description:
      "The Nike Air Max 90 is a timeless classic with unmatched comfort and style.",
    price: 8999,
    image_url:
      "https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/6d742bce-ba92-4e66-8263-0532bbdeb78f/air-force-1-lv8-5-big-kids-shoes-k8Jkw3.png",
  },
  {
    id: 3,
    name: "Nike Air Force 1 '07",
    description:
      "Experience ultimate comfort and energy return with the Adidas Ultraboost.",
    price: 8999,
    image_url:
      "https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/b7d9211c-26e7-431a-ac24-b0540fb3c00f/air-force-1-07-mens-shoes-jBrhbr.png",
  },
  {
    id: 4,
    name: "Nike Air Force 1 '07 (Women's)",
    description:
      "The Puma RS-X combines retro style with modern technology for a unique look.",
    price: 7999,
    image_url:
      "https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/8d752b32-17e8-40bc-ac1a-7a8849957a12/air-force-1-07-womens-shoes-PqdxJw.png",
  },
  {
    id: 5,
    name: "Nike Air Force 1 '07 Next Nature",
    description:
      "The New Balance 990v5 offers premium comfort and classic American craftsmanship.",
    price: 8999,
    image_url:
      "https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/d86cc16f-67d2-4781-a01f-7ea19eeba5cd/air-force-1-07-next-nature-womens-shoes-fvxZ0g.png",
  },
  {
    id: 6,
    name: "Nike Air Force 1 '07 LV8",
    description:
      "The New Balance 990v5 offers premium comfort and classic American craftsmanship.",
    price: 8999,
    image_url:
      "https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/a9b83f5c-af29-49b5-a784-989974e9c531/air-force-1-07-lv8-mens-shoes-3Q0nlJ.png",
  },
];

const PopularSneakers = () => {
  return (
    <RibbonWrapper>
      <RibbonTitle>POPULAR RIGHT NOW</RibbonTitle>
      <RibbonContent>
        {sneakers.map((sneaker) => (
          <SneakerCard key={sneaker.id}>
            <SneakerImage src={sneaker.image_url} alt={sneaker.name} />
            <SneakerInfo>
              <SneakerName>{sneaker.name}</SneakerName>
              <SneakerPrice>${(sneaker.price / 100).toFixed(2)}</SneakerPrice>
            </SneakerInfo>
          </SneakerCard>
        ))}
      </RibbonContent>
    </RibbonWrapper>
  );
};

// const PopularSneakers = () => {
//   const [sneakers, setSneakers] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     const fetchSneakers = async () => {
//       try {
//         setLoading(true);
//         const response = await axios.get(
//           "https://dry-needles-throw.loca.lt/products"
//         );
//         // const response = await axios.get("http://localhost:8001/products");
//         setSneakers(response.data);
//         setLoading(false);
//       } catch (error) {
//         console.error("Error fetching sneakers:", error);
//         setError("Failed to load sneakers. Please try again later.");
//         setLoading(false);
//       }
//     };

//     fetchSneakers();
//   }, []);

//   if (loading) {
//     return <LoadingMessage>Loading popular sneakers...</LoadingMessage>;
//   }

//   if (error) {
//     return <ErrorMessage>{error}</ErrorMessage>;
//   }

//   return (
//     <RibbonWrapper>
//       <RibbonTitle>POPULAR RIGHT NOW</RibbonTitle>
//       <RibbonContent>
//         {sneakers.map((sneaker) => (
//           <SneakerCard key={sneaker.id}>
//             <SneakerImage src={sneaker.image_url} alt={sneaker.name} />
//             <SneakerInfo>
//               <SneakerName>{sneaker.name}</SneakerName>
//               <SneakerPrice>₽{sneaker.price.toFixed(2)}</SneakerPrice>
//             </SneakerInfo>
//           </SneakerCard>
//         ))}
//       </RibbonContent>
//     </RibbonWrapper>
//   );
// };

export default PopularSneakers;
