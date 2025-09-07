function computeGameStateOfTaskEnvironment(taskEnvironment) {
  const { pastActions, currentAction } = taskEnvironment;
  const initialState = getInitialGameState(taskEnvironment);
  let currentState = doActionMoves(initialState, pastActions);
  if (currentAction !== null) {
    currentState = doAction(currentState, currentAction);
  }
  /*
  const someActionsTaken = taskEnvironment.pastActions.length > 0;
  // TODO: DRY identical someActionsTaken computation at two places (or avoid
  // finalGameStage computation altogether, it feels like a hack...)
  const finalGameStage = decideGameStage(
    currentState.fields,
    currentState.spaceship,
    taskEnvironment.interpreting,
    someActionsTaken);
  return { ...currentState, stage: finalGameStage };
  */
  return currentState;
}