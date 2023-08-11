from lib import *



class Simulator:

	def play_one_episode(self, exploration, training=True, rand_price=True, print_t=False):

		state, valid_actions = self.env.reset(rand_price=rand_price)
		done = False
		env_t = 0
		try:
			env_t = self.env.t
		except AttributeError:
			pass

		cum_rewards = [np.nan] * env_t
		actions = [np.nan] * env_t
		states = [None] * env_t
		prev_cum_rewards = 0.

		while not done:
			if print_t:
				print(self.env.t)
    

			action = self.agent.act(state, exploration, valid_actions)
			next_state, reward, done, valid_actions = self.env.step(action)

			cum_rewards.append(prev_cum_rewards+reward)
			prev_cum_rewards = cum_rewards[-1]
			actions.append(action)
			states.append(next_state)

			if training:
				self.agent.remember(state, action, reward, next_state, done, valid_actions)
				self.agent.replay()

			state = next_state

		return cum_rewards, actions, states


	