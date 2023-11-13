import { useState, useEffect, useRef } from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { blue } from '@mui/material/colors';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import PetsIcon from '@mui/icons-material/Pets';
import PublicIcon from '@mui/icons-material/Public';
import StopOutlinedIcon from '@mui/icons-material/StopOutlined';
import { SiPython } from 'react-icons/si';

import loadingCat from '../public/inked_loading_cat.jpg';
import startCat from '../public/startCat.avif';
import avatar from '../public/avatar.webp';

//const mobile = useMediaQuery(theme.breakpoints.down('tablet'));

function Cat({ imgSrc, name, description, origin }) {
  return (
    <Box
      sx={{
        backgroundImage: `url(${imgSrc})`,
        backgroundPosition: 'center',
        backgroundSize: '100% 100%',
        backgroundRepeat: 'no-repeat',
        width: '100%',
        height: '100%',
      }}>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          gap: '20px',
          padding: '40px',
        }}>
        <Typography sx={{ fontWeight: 900, fontSize: '20px', color: 'orange' }}>
          <PetsIcon /> {name} <PetsIcon />
        </Typography>
        <Typography
          sx={{ color: 'dodgerblue', fontWeight: 900, fontSize: '20px' }}>
          <PublicIcon /> {origin} <PublicIcon />
        </Typography>
        <Typography sx={{ color: 'green', fontWeight: 900, fontSize: '20px' }}>
          {description}
        </Typography>
      </Box>
    </Box>
  );
}

function Pygame({
  setLoading,
  catsRef,
  cat = null,
  fetchedAll,
  setFetchedAll,
}) {
  useEffect(() => {
    let subscribed = true;
    if (subscribed && !fetchedAll) {
      setLoading(true);
      fetch('https://api.thecatapi.com/v1/breeds', {
        headers: { 'x-api-key': '7ee9d6b7-120d-475e-899d-7c5cb2353ef9' },
      })
        .then((res) => res.json())
        .then(async (data) => {
          for (const { name, description, origin, image } of data) {
            if (!image) continue;

            switch (name) {
              case 'Bengal':
                {
                  image.url =
                    'https://inspirationseek.com/wp-content/uploads/2014/08/Bengal-Cat-Pictures.jpg';
                }
                break;
              case 'Dragon Li':
                {
                  image.url =
                    'https://www.mascotarios.org/wp-content/uploads/2011/07/Dragon-Li-768x768.jpg';
                }
                break;
              case 'Ocicat':
                {
                  image.url =
                    'https://www.dogalize.com/wp-content/uploads/2017/03/ocicat.jpg';
                }
                break;
            }

            const response = await fetch(
              `https://oqknz96m34.execute-api.us-west-2.amazonaws.com/main?url=${encodeURIComponent(
                image.url
              )}`
            );

            const contentType = response.headers.get('content-type');
            const text = await response.text();
            const imgSrc = `data:${contentType};base64,${text}`;
            catsRef.current.push(
              <Cat
                name={name}
                description={description}
                origin={origin}
                imgSrc={imgSrc}
              />
            );
            if (catsRef.current.length > 0) {
              setLoading(false);
            }
          }
          setFetchedAll();
        });
    }
  }, []);

  return <Box sx={{ flexBasis: '80%' }}>{cat}</Box>;
}

function Start({ run }) {
  return (
    <Box
      sx={{
        backgroundImage: `url(${startCat})`,
        flexBasis: '80%',
        width: '100%',
        height: '100%',
        backgroundRepeat: 'no-repeat',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
      }}>
      <PlayArrowIcon
        onClick={run}
        sx={{
          '&:hover': {
            cursor: 'pointer',
          },
          color: `${blue[500]}`,
          fontSize: 40,
        }}
      />
    </Box>
  );
}

export default function CatFacts() {
  const catsRef = useRef([]);
  const [currCat, setCurrCat] = useState(-1);
  const [running, setRunning] = useState(false);
  const [loading, setLoading] = useState(false);
  const [fetchedAll, setFetchedAll] = useState(false);

  const loadingCatImg = (
    <Box
      component='img'
      src={loadingCat}
      sx={{
        width: '400px',
        height: 'auto',
      }}></Box>
  );

  const intervalFn = (fetchedAll, currCat, n) => {
    console.log('interval fn', fetchedAll, currCat, n);
    if (fetchedAll && currCat === n - 1) {
      setCurrCat(0);
    } else {
      setCurrCat((currCat) => currCat + 1);
    }
  };

  useEffect(() => {
    let id;

    if (running) {
      if (currCat === -1) {
        setCurrCat((currCat) => currCat + 1);
      } else {
        id = setTimeout(() => {
          intervalFn(fetchedAll, currCat, catsRef.current.length);
        }, 3000);
      }
    }

    return () => {
      clearTimeout(id);
    };
  }, [running, currCat]);

  return (
    <Box
      sx={{
        display: 'flex',
        flexDir: 'row',
        backgroundColor: '#0E1525',
        height: '100vh',
        width: '100vw',
      }}>
      {running ? (
        <Pygame
          catsRef={catsRef}
          cat={loading ? loadingCatImg : catsRef.current[currCat]}
          setLoading={setLoading}
          fetchedAll={fetchedAll}
          setFetchedAll={() => setFetchedAll(true)}
        />
      ) : (
        <Start run={() => setRunning(true)} />
      )}
      <Box
        sx={{
          flexBasis: '20%',
          display: 'flex',
          flexDirection: 'column',
          gap: '20px',
        }}>
        <Button
          startIcon={running ? <StopOutlinedIcon /> : <PlayArrowIcon />}
          variant='contained'
          sx={{ width: '100%' }}
          onClick={() => {
            setRunning(!running);
            setCurrCat(0);
            if (running) {
              setLoading(true);
            } else {
              setLoading(false);
            }
          }}>
          {running ? 'Stop' : 'Run'}
        </Button>
        <Box
          sx={{
            padding: '0px 5px',
            display: 'flex',
            flexDirection: 'column',
            gap: '15px',
          }}>
          <Box
            sx={{
              display: 'flex',
              flexDirection: 'row',
              gap: '10px',
              justifyContent: 'center',
              alignItems: 'center',
            }}>
            <SiPython />
            <Typography sx={{ fontSize: '20px', fontWeight: 600 }}>
              catfacts
            </Typography>
          </Box>
          <Box
            sx={{
              display: 'flex',
              flexDirection: 'row',
              gap: '10px',
              justifyContent: 'center',
              alignItems: 'center',
            }}>
            <Box
              component='img'
              src={avatar}
              sx={{
                height: '24px',
                width: '24px',
                borderRadius: '100px',
              }}></Box>
            <Typography sx={{ fontSize: '12px', fontWeight: 300 }}>
              MikeBarberry
            </Typography>
          </Box>
        </Box>
      </Box>
    </Box>
  );
}
